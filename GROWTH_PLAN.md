# Audicap Website Growth Plan

Last updated: 2026-05-16

## Current Diagnosis

Audicap does not currently have a store conversion problem at the Chrome Web Store listing level. The bigger issue is top-of-funnel volume.

Recent Chrome Web Store data showed:

| Period | Impressions | Store page views | Installs | View rate | Install per view |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-04-13 to 2026-05-12 | 380 | 197 | 140 | 51.8% | 71.1% |
| 2026-05-08 to 2026-05-12 | 47 | 21 | 16 | 44.7% | 76.2% |
| 2026-05-10 to 2026-05-12 | 30 | 13 | 11 | 43.3% | 84.6% |

The website is structurally ready for SEO, but the current content is still thin. Existing articles are mostly 300-800 words, which is not enough to build durable long-tail search traffic.

The immediate goal is to grow qualified traffic without repeatedly changing the Chrome Web Store title, summary, or long description.

## Goals

### 14-Day Goals

- Add tracking to all website-to-CWS outbound links.
- Expand the top 3 SEO articles into stronger, more useful pages.
- Add 3 new high-intent pages.
- Submit sitemap and priority pages in Google Search Console.
- Establish a weekly reporting loop for page views, CWS outbound clicks, and installs.

### 30-Day Goals

- Reach 15-20 total SEO pages.
- Increase CWS daily impressions from about 13/day to 50/day.
- Increase website-origin CWS clicks to a measurable baseline.
- Get 3-5 real Chrome Web Store reviews from genuine users.
- Identify which content cluster produces the most qualified clicks.

## Tracking Plan

### Add UTM Parameters To CWS Links

All links from the website to Chrome Web Store should include UTM parameters.

Base URL:

```text
https://chromewebstore.google.com/detail/audicap/cfalkkjbhiohkomajlelefmllnoniloo
```

Recommended pattern:

```text
?utm_source=audicap_website&utm_medium=seo&utm_campaign={page_slug}
```

Examples:

```text
https://chromewebstore.google.com/detail/audicap/cfalkkjbhiohkomajlelefmllnoniloo?utm_source=audicap_website&utm_medium=seo&utm_campaign=home
https://chromewebstore.google.com/detail/audicap/cfalkkjbhiohkomajlelefmllnoniloo?utm_source=audicap_website&utm_medium=seo&utm_campaign=youtube_transcription
https://chromewebstore.google.com/detail/audicap/cfalkkjbhiohkomajlelefmllnoniloo?utm_source=audicap_website&utm_medium=seo&utm_campaign=google_meet_no_bot
```

### Website Analytics Events

If Google Analytics or another web analytics tool is enabled, track:

```text
page_view
outbound_click_to_cws
article_slug
utm_campaign
cta_location
```

Suggested CTA locations:

```text
hero
article_callout
sidebar
footer_cta
pricing
```

### Chrome Extension Funnel

The plugin should be evaluated with this funnel after the new analytics version is published:

```text
extension_installed
extension_opened
popup_loaded
login_clicked
auth_google_success
login_succeeded
recording_started
```

## Content Strategy

The website should be built around four search clusters.

### Cluster 1: YouTube And Video Transcription

Search intent: users want transcripts, subtitles, notes, or translations from YouTube and online videos.

Priority pages:

| URL | Primary keyword | Intent | Priority |
| --- | --- | --- | --- |
| `/blog/transcribe-youtube-video-in-chrome.html` | transcribe YouTube video in Chrome | Existing page to expand | P0 |
| `/use-cases/youtube-transcript-generator.html` | YouTube transcript generator Chrome extension | New landing page | P0 |
| `/blog/youtube-video-to-text-notes.html` | YouTube video to text notes | New article | P1 |
| `/blog/translate-youtube-video-live.html` | translate YouTube video live | New article | P1 |
| `/blog/export-youtube-transcript-srt.html` | export YouTube transcript SRT | New article or merge with SRT page | P2 |

Recommended additions to existing YouTube page:

- Add a step-by-step workflow with screenshots.
- Add a comparison against YouTube auto captions.
- Add examples for students, language learners, and creators.
- Add FAQ for accuracy, subtitle export, translation, and privacy.
- Add one clear CTA near the first third of the article.

### Cluster 2: Meeting Transcription Without Bots

Search intent: users want meeting notes without inviting a bot or changing the meeting workflow.

Priority pages:

| URL | Primary keyword | Intent | Priority |
| --- | --- | --- | --- |
| `/blog/transcribe-google-meet-without-bot.html` | transcribe Google Meet without bot | Existing page to expand | P0 |
| `/blog/transcribe-zoom-web.html` | transcribe Zoom web in Chrome | New article | P0 |
| `/blog/google-meet-transcription-extension.html` | Google Meet transcription extension | New article | P1 |
| `/blog/meeting-transcription-without-bot.html` | meeting transcription without bot | New pillar article | P1 |
| `/alternatives/otter-ai.html` | Otter.ai alternative Chrome audio | Existing page to expand | P1 |

Recommended additions to existing Google Meet page:

- Add a sharper comparison table: captions vs meeting bots vs Chrome tab audio.
- Add a "when this is appropriate" section.
- Add consent and compliance wording without overclaiming.
- Add setup screenshots.
- Add troubleshooting for Chrome tab audio permission.

### Cluster 3: Live Translation

Search intent: users need to understand foreign-language audio as it plays.

Priority pages:

| URL | Primary keyword | Intent | Priority |
| --- | --- | --- | --- |
| `/blog/live-translation-chrome-audio.html` | live translation Chrome audio | Existing page to expand | P0 |
| `/blog/live-captions-translation.html` | live captions translation Chrome | New article | P0 |
| `/use-cases/language-learning-video-translation.html` | video translation for language learners | New landing page | P1 |
| `/blog/translate-online-course-audio.html` | translate online course audio | New article | P1 |

Recommended additions:

- Add concrete examples: YouTube lecture, webinar, podcast, online course.
- Explain when live translation helps and when it will be imperfect.
- Add language learner positioning.
- Add screenshot showing transcript and translation side by side.

### Cluster 4: Pricing And Alternatives

Search intent: users are comparing tools and pricing models.

Priority pages:

| URL | Primary keyword | Intent | Priority |
| --- | --- | --- | --- |
| `/blog/pay-as-you-go-transcription-students.html` | pay as you go transcription | Existing page to expand | P0 |
| `/alternatives/otter-ai.html` | Otter.ai alternative | Existing page to expand | P1 |
| `/alternatives/notta.html` | Notta alternative | New comparison page | P1 |
| `/alternatives/meetgeek.html` | MeetGeek alternative | New comparison page | P2 |
| `/blog/transcription-without-subscription.html` | transcription without subscription | New article | P1 |

Recommended additions:

- Keep comparisons fair and factual.
- Avoid claiming competitors store data insecurely unless sourced.
- Highlight Audicap's specific difference: Chrome tab audio, live translation, pay-as-you-go, no meeting bot.

## Page Quality Standard

Each priority SEO page should follow this structure:

```text
Title
Meta description
Canonical URL
Article schema
FAQ schema where applicable
Clear H1
Short intent-matching intro
Step-by-step workflow
Comparison table
Product screenshot or visual example
Troubleshooting section
FAQ
Internal links to 2-4 related pages
CWS CTA with UTM
```

Recommended length:

```text
P0 pages: 1200-1800 words
P1 pages: 900-1400 words
P2 pages: 700-1000 words
```

## GEO Writing Standard

GEO means Generative Engine Optimization. The goal is not only to rank in traditional search results, but also to make a page easy for AI answer engines to understand, summarize, and cite.

Use GEO as an additional layer on top of SEO, not as a replacement for SEO.

### GEO Page Structure

Every priority page should include:

```text
Quick Answer
Definition or direct explanation
Step-by-step workflow
Comparison table
Concrete use cases
Limitations and caveats
FAQ
Clear product fit statement
```

### GEO Writing Rules

- Answer the primary query in the first 150 words.
- Use factual, compact paragraphs that can stand alone.
- Avoid vague marketing claims such as "best", "perfect", or "zero delay".
- Include tradeoffs and limitations so the content reads as reliable.
- Use tables for comparisons because answer engines can extract them cleanly.
- Use FAQ schema for common direct questions.
- Link to related pages to reinforce topic clusters.
- Keep the product recommendation native to the problem, not forced into every paragraph.

### GEO Example Pattern

```text
Question: Can I transcribe YouTube videos in Chrome?

Answer: Yes. Audicap can capture audio playing in a regular YouTube Chrome tab and generate a live transcript while the video plays. It can also translate the transcript, summarize key points, and export the result as TXT, Markdown, or SRT.

Limitations: Accuracy depends on audio quality, speaker clarity, background noise, and specialized vocabulary. For subtitles or published material, review and edit the transcript before use.
```

### GEO Success Indicators

Track:

```text
Long-tail impressions in Google Search Console
Branded search growth
Referral traffic from AI-search surfaces where available
Direct traffic growth after answer-engine visibility
CWS outbound clicks by article UTM campaign
```

## Internal Linking Rules

Every article should link to:

- One parent collection page, such as `/blog/` or `/alternatives/`.
- Two related blog posts.
- One high-intent conversion page or CWS CTA.
- One relevant alternative/comparison page where natural.

Homepage should link to:

- YouTube transcription page.
- Google Meet without bot page.
- Live translation page.
- Alternatives hub.

## Visual Asset Plan

The current SEO pages need real product visuals. Add screenshots or composed product examples for:

```text
YouTube tab + live transcript
YouTube tab + live translation
Google Meet tab + transcript panel
Export menu showing TXT / Markdown / SRT
Pay-as-you-go credit balance
```

Use optimized images:

```text
Format: webp or compressed png
Width: 1200-1600px for article hero examples
Alt text: descriptive and keyword-relevant
Lazy loading: loading="lazy"
```

## Implementation Roadmap

### Phase 1: Measurement And Existing Page Upgrades

Target: 3-5 days.

Tasks:

- Add UTM parameters to all CWS links.
- Confirm real web analytics IDs are configured.
- Add outbound click tracking if analytics is active.
- Expand `/blog/transcribe-youtube-video-in-chrome.html`.
- Expand `/blog/transcribe-google-meet-without-bot.html`.
- Expand `/blog/live-translation-chrome-audio.html`.
- Update sitemap `lastmod` for changed pages.

Success criteria:

- All CWS clicks can be attributed by source page.
- Top 3 pages are deep enough to submit for indexing.
- Search Console has sitemap and priority URLs submitted.

### Phase 2: New High-Intent Pages

Target: 1 week.

Create:

```text
docs/use-cases/youtube-transcript-generator.html
docs/blog/transcribe-zoom-web.html
docs/blog/live-captions-translation.html
docs/blog/transcription-without-subscription.html
docs/alternatives/notta.html
```

Update:

```text
docs/blog/index.html
docs/alternatives/index.html
docs/sitemap.xml
```

Success criteria:

- 5 new pages published.
- Each page has schema, internal links, and CWS UTM CTA.
- Each page targets one clear search intent.

### Phase 3: Distribution

Target: 1-2 weeks after Phase 1.

Submit to:

```text
Product Hunt
AlternativeTo
SaaSHub
Uneed
BetaList
There is An AI For That
Futurepedia
Toolify
Microlaunch
Webstoreextensions.com
```

Rules:

- Rewrite description per platform.
- Do not copy-paste the exact homepage text.
- Use one primary angle per platform.
- Track submissions in a spreadsheet.

## Reporting Cadence

Weekly report should include:

```text
Google Search Console impressions
Google Search Console clicks
Top queries
Top pages
Website page views
CWS outbound clicks
CWS impressions
CWS page views
CWS installs
PostHog extension_installed
PostHog popup_loaded
PostHog login_succeeded
PostHog recording_started
```

Decision rules:

```text
High GSC impressions, low clicks:
Improve title and meta description for that page.

High page views, low CWS clicks:
Improve article CTA and product proof.

High CWS clicks, low installs:
Improve CWS screenshots, reviews, and trust signals.

High installs, low popup_loaded:
Add post-install onboarding.

High popup_loaded, low login_clicked:
Improve first screen CTA and free-minutes messaging.
```

## Immediate Next Actions

1. Add UTM parameters to website CWS links.
2. Expand the YouTube transcription article first.
3. Expand the Google Meet without bot article second.
4. Add a new `/use-cases/youtube-transcript-generator.html` page.
5. Submit sitemap and priority URLs in Google Search Console.
6. Publish the new plugin analytics version so the install-to-login funnel becomes measurable.
