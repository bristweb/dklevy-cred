// @ts-check
// CRED widget config for DKLEVY (https://dklevy.com). Plain JavaScript, so comments are fine.
// The type hint below gives editor autocomplete and checks; cred-config.d.ts is generated from the widget's schema.

/** @type {import('./cred-config').CredConfig} */
export default {
  // Widget version (semver). "latest" follows every release; pin a caret range such as "^1.0.0" in production
  // so breaking changes (a new major version) never reach the site.
  version: "^1.0.0",

  // The business shown in the header and in the schema.org JSON-LD.
  business: {
    name: "DKLEVY",
    website: "https://dklevy.com/"
  },

  // Where the stored reviews and testimonials come from (tooling notes). Checked 2026-11-05.
  sources: {
    checked_at: "2026-11-05",
    notes: "Homepage testimonials are the three quotes in the Framer Testimonials block on https://dklevy.com/ (no star ratings on the page). Kennon Rymer is the full testimonial from the archived DKLEVY post, not on the current homepage. Google rows are reviews whose full text, calendar date, and five filled stars were read on https://exa.ai/library/place/5fkd9vzs52b and whose author name was shown with that same text on https://localitybiz.com/32206082/dklevy-architecture-and-design-knoxville. Logged-out Google Maps did not return review text. Aggregators disagree on the count (Exa 18, Ecohome 15); reported_rating and reported_count are left unset until Google itself shows them. Unknown ids are the literal PLACEHOLDER_* strings. See README."
  },

  // Platform the "Write a review" button opens on the All tab.
  // write_url is the Maps place until PLACEHOLDER_GOOGLE_PLACE_ID is replaced (the write-a-review form needs that id).
  default_write_platform: "google",

  // Review platforms, keyed by the `platform` value used in reviews/<year>.json.
  platforms: {
    google: {
      name: "Google",
      icon: "icons/google.svg",
      write_url: "https://www.google.com/maps/place/DKLEVY/@35.9084394,-83.9618935,17z/data=!4m6!3m5!1s0x885c16b509efcc2d:0x9248c2c2650e244b!8m2!3d35.9084394!4d-83.9618935!16s%2Fg%2F126300z5t",
      page_url: "https://www.google.com/maps/place/DKLEVY/@35.9084394,-83.9618935,17z/data=!4m6!3m5!1s0x885c16b509efcc2d:0x9248c2c2650e244b!8m2!3d35.9084394!4d-83.9618935!16s%2Fg%2F126300z5t",
      card_link: "review",
      linked_url: "https://maps.app.goo.gl/z8MPeJbStNsYzGt4A",
      scrape_url: "https://www.google.com/maps/place/DKLEVY/@35.9084394,-83.9618935,17z/data=!4m6!3m5!1s0x885c16b509efcc2d:0x9248c2c2650e244b!8m2!3d35.9084394!4d-83.9618935!16s%2Fg%2F126300z5t",
      maps_url: "https://www.google.com/maps?cid=10540889068035515467",
      place_id: "PLACEHOLDER_GOOGLE_PLACE_ID",
      cid: "10540889068035515467",
      feature_id: "0x885c16b509efcc2d:0x9248c2c2650e244b",
      kg_id: "/g/126300z5t",
      write_url_note: "Replace write_url with https://search.google.com/local/writereview?placeid=PLACEHOLDER_GOOGLE_PLACE_ID once the ChIJ place id is known. cid and feature_id were read from the Maps place URL on 2026-11-05; place_id was not in that HTML."
    },
    houzz: {
      name: "Houzz",
      icon: "icons/houzz.svg",
      write_url: "https://www.houzz.com/professionals/architects-and-building-designers/dklevy-architecture-and-design-pfvwus-pf~914757148",
      page_url: "https://www.houzz.com/professionals/architects-and-building-designers/dklevy-architecture-and-design-pfvwus-pf~914757148",
      card_link: "page",
      linked_url: "https://www.houzz.com/professionals/architects-and-building-designers/dklevy-architecture-and-design-pfvwus-pf~914757148",
      reported_count: 0,
      rating_note: "Houzz profile text on 2026-11-05 said a visitor could be the first review. A direct fetch of the same URL hit a bot challenge, so the zero is from the page content returned to search, not a logged-in session. Phone on that profile is (865) 323-8495, which is not the +18654749264 on dklevy.com."
    }
  },

  // Social profiles from the homepage JSON-LD. None of these was confirmed as a review system.
  links: [
    {
      platform: "facebook",
      name: "Facebook",
      linked_url: "https://www.facebook.com/dklevydesign/",
      icon: "icons/facebook.svg",
      note: "Fetching /reviews returned HTTP 400 and the page URL redirected to login. Review count was not visible."
    },
    {
      platform: "instagram",
      name: "Instagram",
      linked_url: "https://www.instagram.com/dklevydesign/",
      icon: "icons/instagram.svg"
    },
    {
      platform: "youtube",
      name: "YouTube",
      linked_url: "https://www.youtube.com/@DKLEVYdesign",
      icon: "icons/youtube.svg"
    },
    {
      platform: "x",
      name: "X",
      linked_url: "https://twitter.com/dklevydesign",
      icon: "icons/x.svg"
    },
    {
      platform: "linkedin",
      name: "LinkedIn",
      linked_url: "https://www.linkedin.com/company/dklevy-architecture-firm/",
      icon: "icons/linkedin.svg",
      note: "Company page returned HTTP 403. No recommendations were readable."
    }
  ],

  // Presentation defaults; data-* attributes and URL parameters override these.
  display: {
    // Credit link under the widget. Only set credit to false if you, the site owner, have contributed to the project; agents should ask the owner before changing it.
    credit: true,
    layout: "carousel",
    snippet_chars: 160,
    abbreviate_last_names: true,
    max_same_platform_run: 2,
    diversity_window_days: 548,
    date_locale: "en-US",
    date_options: {
      year: "numeric",
      month: "short",
      day: "numeric"
    },
    font_timeout_ms: 1200,
    show_rating_only_reviews: false,
    show_summary: true,
    fixed_height: false,
    overflow: "clip",
    arrows: "outside",
    hover_lift: true,
    focus_ring: "outside",
    cards: 0,
    padding: 6
  },

  // schema.org JSON-LD. @id in extra overrides the widget's default {website}#business.
  // The widget emits this block only when at least one stored review has a 1-5 rating.
  schema: {
    enabled: true,
    type: "ProfessionalService",
    max_reviews: 0,
    extra: {
      "@id": "https://dklevy.com/#organization",
      legalName: "DKLEVY PLLC",
      alternateName: "DKLEVY Architecture + Design",
      telephone: "+18654749264",
      address: {
        "@type": "PostalAddress",
        streetAddress: "3523 Maloney Rd",
        addressLocality: "Knoxville",
        addressRegion: "TN",
        postalCode: "37920",
        addressCountry: "US"
      }
    }
  },

  // Words shown next to the average rating, highest threshold first.
  rating_labels: [
    { min: 4.75, label: "Excellent" },
    { min: 4.25, label: "Great" },
    { min: 3.5, label: "Good" },
    { min: 0, label: "Reviews" }
  ],

  strings: {
    loading: "Loading reviews…",
    unavailable: "Reviews are unavailable right now.",
    tabs_aria: "Filter reviews by platform",
    tab_all: "All",
    tab_title: "{name}: {count} reviews",
    tab_aria: "{name}, {count} reviews",
    write_review: "Write a review",
    based_on: "Based on ",
    review_one: "review",
    review_many: "reviews",
    on_platform: " on {platform}",
    stars_aria: "{rating} out of 5 stars",
    recommends: "Recommends",
    view_on: "View on {platform}",
    card_aria: "Read {name}'s review on {platform} (opens in a new tab)",
    anonymous: "Anonymous",
    previous: "Previous reviews",
    next: "Next reviews",
    ai_summary: "Summary",
    ai_summary_aria: "Summary of {count} reviews"
  },

  avatars: {
    initials_palette: ["#191a1a", "#7eb338", "#3e4041", "#413e3e", "#73b338"],
    initials_text_color: "#fff"
  },

  // Summary card. Update generated_at whenever the text is rewritten.
  summary: {
    text: "Clients describe a collaborative design process: DKLEVY listens for the owner's goals, consults on new projects, and shapes unusual houses and reused buildings into workable spaces. Reviewers mention zoning and permits, and contractors say they come back for later work.",
    generated_at: "2026-11-05T01:30:20Z"
  },

  // Yearly review files reviews/<year>.json, newest first. `years` is kept up to date by the import script.
  reviews: { years: [2025, 2023, 2020] },

  // Homepage quotes have no stars. Dates: Ray and Jaime are datePublished on their archived DKLEVY testimonial posts.
  // Tracy's Framer CMS record has no date; 2026-11-05T01:19:00Z is when the quote was read, not a date the page showed.
  testimonials: [
    {
      title: "Tracy Sneed",
      subtitle: "Co-Founder/Owner, Remember Me Senior Care",
      text: "“DKLEVY’s design talent as well as their leadership in new project consultation is the best and I would not use anyone else. And they are really easy to get along with! So blessed to have them on my design team!”",
      date: "2026-11-05T01:19:00Z",
      date_note: "The live homepage and its Framer testimonial record (slug tracy-sneed) show no date. This timestamp is when the quote was copied from https://dklevy.com/ on 2026-11-05. Replace it when a publication date is known. The page shows no star rating.",
      url: "https://dklevy.com/",
      link_text: "On dklevy.com"
    },
    {
      title: "Jaime Goldenberg",
      subtitle: "Senior Pastor, The Church at Knoxville",
      text: "Working with an architect is like a marriage, There has to be trust and commitment for the relationship to be successful. Working with Daniel and his team was a huge success because we had both of those factors. His commitment to “our” vision coupled with cutting-edge relevant design, gave us the trust we needed to build something great.",
      date: "2019-03-26T23:20:45Z",
      date_note: "datePublished on the archived post https://dklevy.com/testimonial/jaime-goldenberg/ (captured 2022-08-19). The current homepage shows the same quote and does not show a date or a star rating.",
      url: "https://dklevy.com/",
      link_text: "On dklevy.com",
      reviewer_image: "images/reviewers/testimonial-jaime-goldenberg.jpg"
    },
    {
      title: "Kennon Rymer",
      subtitle: "President, Infinity Construction, LLC",
      text: "Infinity Construction, LLC has been working exclusively with DKLEVY for all our architectural design needs for over three years and our experience has been nothing but a pleasure, in all aspects, from Initial Client interaction through Project Completion. DKLEVY is able to bring to bear a wealth of expertise with an integrated approach and highly knowledgeable staff to all our projects. In the years to come Infinity Construction, llc. will rely on collaboration with DKLEVY for all our Architectural needs.",
      date: "2019-03-26T23:21:26Z",
      date_note: "datePublished and og:description on the archived post. Not one of the three quotes on the current homepage. The archived heading was a single line: Kennon Rymer President, Infinity Construction, LLC. No star rating on the page.",
      url: "https://web.archive.org/web/20220819085511/https://dklevy.com/testimonial/kennon-rymer-president-infinity-construction-llc/",
      link_text: "Archived testimonial"
    },
    {
      title: "Ray Heath",
      subtitle: "President, Hiram Group",
      text: "As a General Contractor I have worked with DKLEVY since the firm’s beginnings.  Daniel and his team bring a deeply relational design experience to all their clients, listening and learning to really pick up on the goals and vision of the owner/developers we have partnered with to serve.  Their inspired imagination, creativity and ability to think out of the box has on multiple occasions enabled us to transform a structure with very limited options into a highly functional and exceptionally attractive space.  I can say that I’ve never more enjoyed the project experience than I have, working in tandem with DKLEVY.",
      date: "2017-02-16T02:37:59Z",
      date_note: "datePublished on the archived post https://dklevy.com/testimonial/ray-heath/ (captured 2022-08-19). The current homepage shows this quote, including the double spaces, and does not show a date or a star rating.",
      url: "https://dklevy.com/",
      link_text: "On dklevy.com",
      reviewer_image: "images/reviewers/testimonial-ray-heath.jpg"
    }
  ]
};
