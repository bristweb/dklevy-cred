#!/usr/bin/env python3
"""DKLEVY review sync: fetch recent reviews from platforms configured in config.js and add only NEW ones.

  python3 scripts/pull_reviews.py --print-inputs
  python3 scripts/pull_reviews.py --from-raw
  APIFY_TOKEN=... python3 scripts/pull_reviews.py

What to scrape comes from config.js `platforms` (`scrape_url`). A platform with no scrape_url, or a scrape_url
that still contains PLACEHOLDER, is skipped.
  Google   -> Apify `compass/Google-Maps-Reviews-Scraper` (logged-out Google Maps shows no review text).
  Yelp     -> Apify `web_wanderer/yelp-reviews-scraper` when a Yelp scrape_url is set.
  Facebook -> Apify `apify/facebook-reviews-scraper` when a Facebook scrape_url is set.
Each Apify run asks only for reviews newer than (latest stored review on that platform - since-days) and is capped
with maxTotalChargeUsd. Raw results live in .pull/ (git-ignored). Then import_reviews.py adds new reviews only.
"""
import argparse, datetime, json, os, subprocess, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from import_reviews import load_reviews  # noqa: E402
import cred_config  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--data', default=os.path.dirname(HERE), help='data repo checkout (default: this repo)')
ap.add_argument('--since-days', type=int, default=30, help='overlap window before the newest stored review')
ap.add_argument('--max-usd', type=float, default=0.5, help='Apify cost cap per actor run (Apify minimum is $0.50)')
ap.add_argument('--all', action='store_true', help='full re-pull (no date window)')
ap.add_argument('--print-inputs', action='store_true', help='print {platform: {actor, input}} and exit')
ap.add_argument('--from-raw', action='store_true',
                help='do not call Apify; import .pull/<platform>.json files saved by another runner')
A = ap.parse_args()
ROOT = os.path.abspath(A.data)
RAW = os.path.join(ROOT, '.pull')
CONFIG = cred_config.load(ROOT)
_PL = CONFIG.get('platforms', {})


def usable(url):
    return bool(url) and 'PLACEHOLDER' not in str(url)


SCRAPE = {k: p.get('scrape_url') for k, p in _PL.items() if usable(p.get('scrape_url'))}
ACTORS = {}
if SCRAPE.get('google'):
    ACTORS['google'] = ('compass~Google-Maps-Reviews-Scraper', lambda since: {
        'startUrls': [{'url': SCRAPE['google']}],
        'maxReviews': 500, 'reviewsSort': 'newest', 'language': 'en', 'reviewsOrigin': 'all',
        'personalData': True, **({'reviewsStartDate': since} if since else {})})
if SCRAPE.get('yelp'):
    ACTORS['yelp'] = ('web_wanderer~yelp-reviews-scraper', lambda since: {
        'biz_urls': [SCRAPE['yelp']],
        'reviews_limit': 200, 'reviews_sort': 'newest', 'include_personal_data': True,
        **({'date_from': since} if since else {})})
if SCRAPE.get('facebook'):
    ACTORS['facebook'] = ('apify~facebook-reviews-scraper', lambda since: {
        'startUrls': [{'url': SCRAPE['facebook']}],
        'resultsLimit': 100, **({'onlyReviewsNewerThan': since} if since else {})})


def pull_apify(actor, inputs, token, max_usd, path):
    items = []
    for inp in inputs if isinstance(inputs, list) else [inputs]:
        qs = urllib.parse.urlencode({'token': token, 'format': 'json', 'clean': '1',
                                     'maxTotalChargeUsd': max_usd, 'timeout': 600})
        url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?{qs}'
        req = urllib.request.Request(url, data=json.dumps(inp).encode(), method='POST',
                                     headers={'Content-Type': 'application/json'})
        items += json.loads(urllib.request.urlopen(req, timeout=660).read())
    json.dump(items, open(path, 'w'))
    return len(items)


def latest_dates(reviews):
    out = {}
    for r in reviews:
        out[r['platform']] = max(out.get(r['platform'], ''), r['date'])
    return out


def main():
    a = A
    os.makedirs(RAW, exist_ok=True)
    token = os.environ.get('APIFY_TOKEN')
    latest = latest_dates(load_reviews(ROOT))

    def since_for(plat):
        if a.all or plat not in latest:
            return None
        dt = datetime.datetime.fromisoformat(latest[plat].replace('Z', '+00:00')) - datetime.timedelta(days=a.since_days)
        return dt.date().isoformat()

    if a.print_inputs:
        print(json.dumps({p: {'actor': act.replace('~', '/'), 'input': b(since_for(p)),
                              'maxTotalChargeUsd': a.max_usd, 'save_items_to': os.path.join(RAW, f'{p}.json')}
                          for p, (act, b) in ACTORS.items()}, indent=2))
        return
    apify_args = []
    if not ACTORS:
        sys.exit('nothing to scrape (set a real scrape_url in config.js)')
    for plat, (actor, build) in ACTORS.items():
        path = os.path.join(RAW, f'{plat}.json')
        if a.from_raw:
            if os.path.exists(path):
                print(f'{plat}: importing {path}')
                apify_args += [f'--{plat}', path]
            else:
                print(f'{plat}: no {path}, skipped')
            continue
        if not token:
            print(f'{plat}: skipped (no APIFY_TOKEN)')
            continue
        since = since_for(plat)
        try:
            print(f'{plat} (apify {actor}, since {since or "all"}):', pull_apify(actor, build(since), token, a.max_usd, path), 'items')
            apify_args += [f'--{plat}', path]
        except Exception as e:
            print(f'{plat} failed:', e, file=sys.stderr)
    if not apify_args:
        sys.exit('nothing pulled')
    subprocess.run([sys.executable, os.path.join(HERE, 'import_reviews.py'), '--data', ROOT, *apify_args], check=True)
    check_summary()


def check_summary():
    revs = load_reviews(ROOT)
    summ = cred_config.load(ROOT).get('summary') or {}
    gen = summ.get('generated_at') or ''
    ts = lambda s: datetime.datetime.fromisoformat(s.replace('Z', '+00:00')) if s else None
    g = ts(gen)
    newer = [r for r in revs if g is None or any(ts(r.get(k)) and ts(r.get(k)) > g for k in ('date', 'collected_at'))]
    if summ.get('text') and not newer:
        print(f'summary: up to date ({len(revs)} reviews, generated {gen})')
        return
    path = os.path.join(RAW, 'summary_input.txt')
    with open(path, 'w') as f:
        for r in sorted(revs, key=lambda r: r['date'], reverse=True):
            if (r.get('text') or '').strip():
                f.write(f"[{r['platform']} {r['date'][:10]} rating={r.get('rating')}] {' '.join(r['text'].split())}\n")
    print(f"SUMMARY STALE: {len(newer)} review(s) dated/collected after config.js summary.generated_at ({gen or 'missing'}). "
          f"Rewrite summary.text from {path} and set summary.generated_at to now (see README).")


if __name__ == '__main__':
    main()
