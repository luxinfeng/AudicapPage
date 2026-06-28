import os
import glob
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time

LANGUAGES = {
    'ja': 'Japanese',
    'de': 'German',
    'fr': 'French',
}

SOURCE_FILES = [
    'docs/blog/export-transcript-to-srt.html',
    'docs/blog/summarize-long-youtube-videos.html',
]

def translate_html(filepath, target_lang):
    print(f"Translating {filepath} to {target_lang}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    translator = GoogleTranslator(source='en', target=target_lang)

    def translate_text(text):
        if not text or not text.strip():
            return text
        try:
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            time.sleep(1)
            return text

    # Translate title
    if soup.title and soup.title.string:
        soup.title.string = translate_text(soup.title.string)

    # Translate meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        meta_desc['content'] = translate_text(meta_desc['content'])

    # Translate og tags
    for og in soup.find_all('meta', attrs={'property': ['og:title', 'og:description']}):
        if og.get('content'):
            og['content'] = translate_text(og['content'])

    # Translate body text tags
    tags_to_translate = ['h1', 'h2', 'h3', 'h4', 'p', 'li', 'span', 'a', 'th', 'td', 'summary']
    for tag_name in tags_to_translate:
        for tag in soup.find_all(tag_name):
            # Only translate if it has direct text content (no nested elements like nested spans)
            if tag.string and tag.string.strip():
                # Skip nav/header/footer to prevent breaking layout or logo, but for SEO it's fine.
                # Let's just translate all direct strings
                tag.string.replace_with(translate_text(tag.string))

    # Fix canonical and hreflang links
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        old_href = canonical['href']
        new_href = old_href.replace('https://audicap.work/', f'https://audicap.work/{target_lang}/')
        canonical['href'] = new_href
    
    # Update lang attribute
    if soup.html:
        soup.html['lang'] = target_lang

    # Write output
    relative_path = filepath.replace('docs/', '')
    output_dir = os.path.join('docs', target_lang, os.path.dirname(relative_path))
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, os.path.basename(filepath))
    with open(output_path, 'w', encoding='utf-8') as f:
        # Use HTML5 formatter to avoid self-closing tags issues
        f.write(soup.prettify(formatter="html5"))
    print(f"Saved to {output_path}")

for filepath in SOURCE_FILES:
    for lang in LANGUAGES.keys():
        translate_html(filepath, lang)
        time.sleep(2) # rate limit prevention

print("Translation completed.")
