#!/usr/bin/env python3
"""
Batch SEO fixes for AudicapPage:
1. Fix duplicate title on use-cases/index.html
2. Add og:type to use-cases/index.html
3. Add Twitter Card to all pages missing it
4. Add hreflang (en + x-default) to 6 new use-case pages
5. Add Clarity tracking to all pages missing it
6. Add 6 i18n pages to sitemap.xml
7. Fix JSON-LD language in ja/de/fr pages
"""

import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"

CLARITY_SNIPPET = """
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    window.addEventListener('DOMContentLoaded', function() {
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window,document,"clarity","script","xdkqvqf653");
    });
  </script>"""

GA_SNIPPET = """
  <!-- Google Analytics (GA4) -->
  <script defer src="https://www.googletagmanager.com/gtag/js?id=G-04VJZMNQV9"></script>
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      window.dataLayer = window.dataLayer || [];
      function gtag(){window.dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-04VJZMNQV9');
    });
  </script>"""


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")
    print(f"  WRITTEN: {path}")


def inject_before_body_close(content, snippet):
    return content.replace("</body>", snippet + "\n</body>", 1)


def inject_tracking_before_body(content):
    if "googletagmanager.com/gtag" not in content:
        content = inject_before_body_close(content, GA_SNIPPET)
    if "clarity.ms" not in content:
        content = inject_before_body_close(content, CLARITY_SNIPPET)
    return content


def extract_og(content, prop):
    m = re.search(rf'<meta property="og:{prop}" content="([^"]*)"', content)
    return m.group(1) if m else ""


def inject_twitter_card(content):
    if 'twitter:card' in content:
        return content
    title = extract_og(content, "title")
    desc = extract_og(content, "description")
    card_html = (
        f'  <!-- Twitter Card -->\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{title}">\n'
        f'  <meta name="twitter:description" content="{desc}">\n'
        f'  <meta name="twitter:image" content="https://audicap.work/og-share.png">'
    )
    match = re.search(r'<meta property="og:image"[^>]*>', content)
    if match:
        insert_pos = match.end()
        return content[:insert_pos] + "\n" + card_html + content[insert_pos:]
    return content


def add_hreflang(content, canonical_url):
    if 'hreflang' in content:
        return content
    hreflang_block = (
        f'\n  <link rel="alternate" hreflang="en" href="{canonical_url}">'
        f'\n  <link rel="alternate" hreflang="x-default" href="{canonical_url}">'
    )
    canonical_pattern = rf'(<link rel="canonical" href="{re.escape(canonical_url)}"[^>]*>)'
    match = re.search(canonical_pattern, content)
    if match:
        insert_pos = match.end()
        return content[:insert_pos] + hreflang_block + content[insert_pos:]
    return content


# ── FIX 1: use-cases/index.html ──
print("\n[FIX 1] Unique title + og:type on use-cases/index.html")
path = DOCS / "use-cases/index.html"
content = read(path)
content = content.replace(
    "<title>Live Transcription for Online Courses &amp; Professional Training | Audicap</title>",
    "<title>Audicap for Professional Learning: Coursera, Canvas, HubSpot &amp; More</title>"
)
if 'og:type' not in content:
    content = content.replace(
        '  <meta property="og:title"',
        '  <meta property="og:type" content="website">\n  <meta property="og:title"'
    )
content = inject_twitter_card(content)
content = inject_tracking_before_body(content)
write(path, content)


# ── FIX 2+3+5: 6 use-case platform pages ──
print("\n[FIX 2+3+5] 6 use-case pages – hreflang + Twitter Card + tracking")
USE_CASE_PAGES = {
    "coursera-transcription.html": "https://audicap.work/use-cases/coursera-transcription.html",
    "udemy-course-transcription.html": "https://audicap.work/use-cases/udemy-course-transcription.html",
    "canvas-lecture-transcription.html": "https://audicap.work/use-cases/canvas-lecture-transcription.html",
    "medical-training-transcription.html": "https://audicap.work/use-cases/medical-training-transcription.html",
    "hubspot-certification-notes.html": "https://audicap.work/use-cases/hubspot-certification-notes.html",
    "interpreter-training-transcription.html": "https://audicap.work/use-cases/interpreter-training-transcription.html",
}
for filename, canonical_url in USE_CASE_PAGES.items():
    path = DOCS / "use-cases" / filename
    if not path.exists():
        print(f"  MISSING: {filename}")
        continue
    content = read(path)
    content = add_hreflang(content, canonical_url)
    content = inject_twitter_card(content)
    content = inject_tracking_before_body(content)
    write(path, content)


# ── FIX 3+5: professional-learning.html ──
print("\n[FIX 3+5] professional-learning.html – Twitter Card + tracking")
path = DOCS / "use-cases/professional-learning.html"
content = read(path)
content = inject_twitter_card(content)
content = inject_tracking_before_body(content)
write(path, content)


# ── FIX 3+5: Blog pages ──
print("\n[FIX 3+5] Blog pages – Twitter Card + tracking")
for path in sorted((DOCS / "blog").glob("*.html")):
    content = read(path)
    content = inject_twitter_card(content)
    content = inject_tracking_before_body(content)
    write(path, content)


# ── FIX 3+5: Alternatives pages ──
print("\n[FIX 3+5] Alternatives pages – Twitter Card + tracking")
for path in sorted((DOCS / "alternatives").glob("*.html")):
    content = read(path)
    content = inject_twitter_card(content)
    content = inject_tracking_before_body(content)
    write(path, content)


# ── FIX 6: sitemap.xml ──
print("\n[FIX 6] sitemap.xml – add 6 i18n pages")
sitemap_path = DOCS / "sitemap.xml"
sitemap = read(sitemap_path)
new_urls = [
    "https://audicap.work/ja/blog/export-transcript-to-srt.html",
    "https://audicap.work/ja/blog/summarize-long-youtube-videos.html",
    "https://audicap.work/de/blog/export-transcript-to-srt.html",
    "https://audicap.work/de/blog/summarize-long-youtube-videos.html",
    "https://audicap.work/fr/blog/export-transcript-to-srt.html",
    "https://audicap.work/fr/blog/summarize-long-youtube-videos.html",
]
entries = ""
for url in new_urls:
    if url not in sitemap:
        entries += (
            f"  <url>\n    <loc>{url}</loc>\n"
            f"    <lastmod>2026-06-28</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.5</priority>\n  </url>\n"
        )
if entries:
    sitemap = sitemap.replace("</urlset>", entries + "</urlset>")
    write(sitemap_path, sitemap)
    print("  Added 6 i18n URLs to sitemap")
else:
    print("  All i18n URLs already present")


# ── FIX 7: i18n JSON-LD language ──
print("\n[FIX 7] Fix i18n pages JSON-LD (headline + description + mainEntityOfPage)")
I18N_FIXES = {
    "ja/blog/export-transcript-to-srt.html": {
        "lang": "ja",
        "headline": "ChromeでオーディオトランスクリプトをSRTにエクスポートする方法",
        "description": "ChromeからオーディオトランスクリプトをSRTファイルに直接エクスポートする方法を学びましょう。",
        "canonical": "https://audicap.work/ja/blog/export-transcript-to-srt.html",
    },
    "ja/blog/summarize-long-youtube-videos.html": {
        "lang": "ja",
        "headline": "長いYouTube動画を要約する方法",
        "description": "Chrome拡張機能を使って長いYouTube動画をリアルタイムで文字起こし・要約する方法を学びましょう。",
        "canonical": "https://audicap.work/ja/blog/summarize-long-youtube-videos.html",
    },
    "de/blog/export-transcript-to-srt.html": {
        "lang": "de",
        "headline": "Audio-Transkripte als SRT in Chrome exportieren",
        "description": "Erfahren Sie, wie Sie Audio-Transkripte direkt aus Chrome als SRT-Dateien exportieren koennen.",
        "canonical": "https://audicap.work/de/blog/export-transcript-to-srt.html",
    },
    "de/blog/summarize-long-youtube-videos.html": {
        "lang": "de",
        "headline": "Lange YouTube-Videos zusammenfassen in Chrome",
        "description": "Lernen Sie, wie Sie lange YouTube-Videos mit einer Chrome-Erweiterung transkribieren und zusammenfassen.",
        "canonical": "https://audicap.work/de/blog/summarize-long-youtube-videos.html",
    },
    "fr/blog/export-transcript-to-srt.html": {
        "lang": "fr",
        "headline": "Exporter des transcriptions audio en SRT dans Chrome",
        "description": "Apprenez a exporter des transcriptions audio directement depuis Chrome en fichiers SRT.",
        "canonical": "https://audicap.work/fr/blog/export-transcript-to-srt.html",
    },
    "fr/blog/summarize-long-youtube-videos.html": {
        "lang": "fr",
        "headline": "Resumer les longues videos YouTube dans Chrome",
        "description": "Apprenez a transcrire et resumer de longues videos YouTube en temps reel avec Chrome.",
        "canonical": "https://audicap.work/fr/blog/summarize-long-youtube-videos.html",
    },
}
for rel_path, meta in I18N_FIXES.items():
    path = DOCS / rel_path
    if not path.exists():
        print(f"  MISSING: {rel_path}")
        continue
    content = read(path)
    en_url = meta["canonical"].replace(f"/{meta['lang']}/", "/")
    content = content.replace(
        f'"mainEntityOfPage":"{en_url}"',
        f'"mainEntityOfPage":"{meta["canonical"]}"'
    )
    content = re.sub(r'"headline":"[^"]*"', f'"headline":"{meta["headline"]}"', content, count=1)
    content = re.sub(r'"description":"[^"]*"', f'"description":"{meta["description"]}"', content, count=1)
    write(path, content)

print("\nAll SEO fixes complete!")
