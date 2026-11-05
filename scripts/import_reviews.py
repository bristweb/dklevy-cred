#!/usr/bin/env python3
"""Normalize raw scraper output into review records (reviews/<year>.json).

Usage (from the repo root; --data defaults to this repo):
  python3 scripts/import_reviews.py --google .pull/google.json --yelp .pull/yelp.json --facebook .pull/facebook.json

Raw inputs:
  google   : Apify compass/Google-Maps-Reviews-Scraper dataset items (JSON array)
  yelp     : Apify web_wanderer/yelp-reviews-scraper dataset items
  facebook : Apify apify/facebook-reviews-scraper dataset items

A review is identified by (platform, platform_review_id). By default only NEW reviews are added; --update also
refreshes existing ones (they keep collected_at, their avatar and a hand-set featured_on_website flag).
A platform is skipped when it is missing from config.js or its scrape_url contains PLACEHOLDER.
"""
import argparse, datetime, hashlib, html, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cred_config  # noqa: E402

NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = CONFIG = PLATFORMS = None
REVIEW_PAGE, PALETTE, INITIALS_TEXT = {}, ['#555555'], '#fff'


def dump(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def init(data_dir):
    global ROOT, CONFIG, PLATFORMS, REVIEW_PAGE, PALETTE, INITIALS_TEXT
    ROOT = os.path.abspath(data_dir)
    CONFIG = cred_config.load(ROOT)
    PLATFORMS = CONFIG.get('platforms', {})
    REVIEW_PAGE = {k: v.get('page_url') for k, v in PLATFORMS.items()}
    av = CONFIG.get('avatars', {})
    PALETTE = av.get('initials_palette') or ['#555555']
    INITIALS_TEXT = av.get('initials_text_color', '#fff')


def load_reviews(data_dir=None):
    root = os.path.abspath(data_dir) if data_dir else ROOT
    cfg = CONFIG if not data_dir else cred_config.load(root)
    out = []
    for y in (cfg.get('reviews') or {}).get('years', []):
        with open(os.path.join(root, 'reviews', f'{y}.json')) as f:
            out += json.load(f)
    return out


def safe_id(s):
    return re.sub(r'[^A-Za-z0-9_-]', '_', str(s))


def display_name(name):
    n = re.sub(r'\(.*?\)', ' ', name or '').strip()
    words = [w for w in re.split(r'\s+', n) if w]
    if not words:
        return 'Anonymous'
    fix = lambda w: w if w.isupper() and len(w) <= 2 else w.capitalize() if w.isupper() or w.islower() else w
    if len(words) == 1:
        return fix(words[0])
    first, last = words[:-1], words[-1]
    if not (len(first) >= 3 and first[1].lower() in ('and', '&')):
        first = first[:1]
    first = ['&' if w.lower() in ('and', '&') else fix(w) for w in first]
    return ' '.join(first) + ' ' + last[0].upper() + '.'


def initials_svg(name, path):
    parts = [p for p in re.split(r'[\s.]+', re.sub(r'\(.*?\)', '', name or '')) if p and p[0].isalpha()]
    ini = (''.join(p[0] for p in parts[:2]) or '?').upper()
    color = PALETTE[int(hashlib.md5((name or '').encode()).hexdigest(), 16) % len(PALETTE)]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="{html.escape(name or "")}">'
           f'<rect width="120" height="120" rx="60" fill="{color}"/>'
           f'<text x="60" y="60" dy=".35em" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
           f'font-size="46" font-weight="600" fill="{INITIALS_TEXT}">{html.escape(ini)}</text></svg>')
    with open(path, 'w') as f:
        f.write(svg)


def fetch_avatar(url, base):
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data, ctype = r.read(), r.headers.get('Content-Type', '')
        ext = '.png' if 'png' in ctype else '.webp' if 'webp' in ctype else '.jpg'
        rel = f'images/reviewers/{base}{ext}'
        with open(os.path.join(ROOT, rel), 'wb') as f:
            f.write(data)
        return rel
    except Exception as e:
        print('avatar failed', base, e, file=sys.stderr)
        return None


def iso(d):
    if isinstance(d, (int, float)):
        return datetime.datetime.fromtimestamp(d / 1000, datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    dt = datetime.datetime.fromisoformat(str(d).replace('Z', '+00:00'))
    return dt.astimezone(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def reply(text, date):
    return {'text': text, 'date': iso(date) if date else None} if text else None


def from_google(x):
    photo = x.get('reviewerPhotoUrl')
    return dict(platform='google', pid=x['reviewId'], name=x.get('name'), photo=photo,
                photo_dl=re.sub(r'=s\d+.*$', '=s160-c', photo) if photo else None,
                profile=x.get('reviewerUrl'), rating=x.get('stars'),
                text=x.get('text') or '', date=iso(x['publishedAtDate']),
                url=x.get('reviewUrl') or REVIEW_PAGE.get('google'),
                reply=reply(x.get('responseFromOwnerText'), x.get('responseFromOwnerDate')),
                extra={'reviewer_review_count': x.get('reviewerNumberOfReviews'),
                       'reviewer_is_local_guide': x.get('isLocalGuide'),
                       'review_image_urls': x.get('reviewImageUrls') or None,
                       'language': x.get('originalLanguage')})


def from_yelp(x):
    a = x.get('author') or {}
    pr = x.get('publicReply') or {}
    return dict(platform='yelp', pid=x['reviewEncid'], name=a.get('name'), photo=a.get('profile_photo'),
                profile=None, rating=x.get('rating'), text=x.get('text') or '', date=iso(x['reviewDate']),
                url=x.get('reviewUrl') or REVIEW_PAGE.get('yelp'),
                reply=reply(pr.get('text'), pr.get('created_at')),
                extra={'reviewer_review_count': a.get('review_count'),
                       'review_image_urls': [ph.get('url') for ph in x.get('photos') or [] if ph.get('url')] or None,
                       'language': x.get('language')})


def fb_star_tag(tags):
    """A star value is stored only when Facebook itself shows one (a tag like '5 stars'). Never inferred from 'recommends'."""
    for t in tags or []:
        m = re.fullmatch(r'\s*([1-5])\s*stars?\s*', str(t), re.I)
        if m:
            return int(m.group(1)), t
    return None, None


def from_facebook(x):
    u = x.get('user') or {}
    stars, tag = fb_star_tag(x.get('tags'))
    return dict(platform='facebook', pid=x['id'], name=u.get('name'), photo=u.get('profilePic'),
                profile=u.get('profileUrl'), rating=stars, text=x.get('text') or '', date=iso(x['date']),
                url=x.get('url') or REVIEW_PAGE.get('facebook'), reply=None,
                extra={'recommended': bool(x.get('isRecommended')), 'tags': x.get('tags') or None,
                       'rating_source': f'facebook recommendation tag "{tag}"' if tag else None})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default=REPO, help='data repo checkout (default: this repo)')
    for p in ('google', 'yelp', 'facebook'):
        ap.add_argument('--' + p)
    ap.add_argument('--update', action='store_true',
                    help='also refresh reviews that already exist (default: add new reviews only)')
    a = ap.parse_args()
    init(a.data)
    os.makedirs(os.path.join(ROOT, 'reviews'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'images', 'reviewers'), exist_ok=True)
    reviews = load_reviews()
    index = {(r['platform'], r['platform_review_id']): i for i, r in enumerate(reviews)}
    conv = {'google': from_google, 'yelp': from_yelp, 'facebook': from_facebook}
    n = 0
    for plat, fn in conv.items():
        path = getattr(a, plat)
        if not path:
            continue
        platform = PLATFORMS.get(plat) or {}
        if not platform:
            print(f'{plat}: not in config.js platforms, skipped', file=sys.stderr)
            continue
        if 'PLACEHOLDER' in str(platform.get('scrape_url') or ''):
            print(f'{plat}: scrape_url is still a placeholder, skipped', file=sys.stderr)
            continue
        with open(path) as f:
            items = json.load(f)
        for x in items:
            r = fn(x)
            if r is None:
                continue
            key = (plat, r['pid'])
            pos = index.get(key)
            if pos is not None and not a.update:
                continue
            old = reviews[pos] if pos is not None else {}
            img = old.get('reviewer_image')
            if not (img and os.path.exists(os.path.join(ROOT, img))):
                stem = f'{plat}-{safe_id(r["pid"])}'
                img = fetch_avatar(r.get('photo_dl') or r['photo'], stem)
                if not img:
                    img = f'images/reviewers/{stem}.svg'
                    initials_svg(display_name(r['name']), os.path.join(ROOT, img))
            rec = {
                'platform': plat,
                'platform_review_id': r['pid'],
                'reviewer_name': r['name'],
                'reviewer_profile_url': r['profile'],
                'reviewer_image': img,
                'reviewer_image_source_url': r['photo'],
                'rating': r['rating'],
                'text': r['text'],
                'date': r['date'],
                'review_url': r['url'],
                'owner_reply': r['reply'],
                'collected_at': old.get('collected_at') or NOW,
            }
            if old:
                rec['updated_at'] = NOW
            rec.update({k: v for k, v in r['extra'].items() if v not in (None, '', []) and not (v is False and k != 'verified_purchase')})
            if old.get('featured_on_website'):
                rec['featured_on_website'] = True
            if pos is None:
                index[key] = len(reviews)
                reviews.append(rec)
            else:
                reviews[pos] = rec
            n += 1
            print('  +' if not old else '  ~', plat, r['date'][:10], display_name(r['name']))
    if n:
        save(reviews)
    print(f'wrote {n} reviews ({"add+update" if a.update else "new only"})')


def save(reviews):
    by_year = {}
    for r in reviews:
        by_year.setdefault(r['date'][:4], []).append(r)
    for y, lst in by_year.items():
        lst.sort(key=lambda r: r['date'], reverse=True)
        dump(lst, os.path.join(ROOT, 'reviews', f'{y}.json'))
    years = sorted((int(y) for y in by_year), reverse=True)
    if (CONFIG.get('reviews') or {}).get('years') != years:
        CONFIG.setdefault('reviews', {})['years'] = years
        cred_config.set_years(ROOT, years)
        print('config.js reviews.years ->', years)


if __name__ == '__main__':
    main()
