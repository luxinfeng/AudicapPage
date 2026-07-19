import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

OLD_DOCS = Path('old_docs')
PAGES_DIR = Path('src/pages')

def fix_links(soup, current_path):
    # Convert relative links like ../ or index.html to absolute /...
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http') or href.startswith('#') or href.startswith('mailto:'):
            continue
        
        # Resolve relative to current_path
        # E.g. old_docs/use-cases/index.html -> current_path is old_docs/use-cases
        # href is ../blog/index.html
        # Resolved should be /blog/
        
        if href == 'index.html':
            if current_path == OLD_DOCS:
                a['href'] = '/'
            else:
                a['href'] = '/' + str(current_path.relative_to(OLD_DOCS)) + '/'
            continue
            
        if href.endswith('index.html'):
            href = href.replace('index.html', '')
            
        if href.endswith('.html'):
            href = href.replace('.html', '')
            
        if href.startswith('../'):
            # simple fix for depth 1
            if current_path.parent == OLD_DOCS:
                a['href'] = '/' + href[3:]
            elif current_path.parent.parent == OLD_DOCS:
                a['href'] = '/' + href[6:]
        elif not href.startswith('/'):
            # relative to current dir
            rel = str(current_path.relative_to(OLD_DOCS))
            if rel == '.':
                a['href'] = '/' + href
            else:
                a['href'] = '/' + rel + '/' + href
                
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('../'):
            img['src'] = '/' + src[3:]
        elif not src.startswith('/') and not src.startswith('http'):
            img['src'] = '/' + src

def migrate():
    for root, dirs, files in os.walk(OLD_DOCS):
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = Path(root) / file
            if filepath == OLD_DOCS / 'index.html':
                continue # Already done manually
                
            print(f"Migrating {filepath}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract Meta
            title = soup.title.string if soup.title else ""
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            description = desc_tag['content'] if desc_tag else ""
            
            canonical_tag = soup.find('link', rel='canonical')
            canonical = canonical_tag['href'] if canonical_tag else ""
            
            hreflangs = []
            for h in soup.find_all('link', rel='alternate', hreflang=True):
                hreflangs.append({'lang': h['hreflang'], 'url': h['href']})
                
            # Extract head scripts (JSON-LD, custom meta)
            head_extras = []
            for script in soup.head.find_all('script', type='application/ld+json'):
                head_extras.append(str(script).replace('<script', '<script is:inline'))
                
            # Extract keywords or specific metas
            keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            if keywords_tag:
                head_extras.append(str(keywords_tag))
                
            # Extract Main content
            main = soup.find('main')
            if not main:
                # Some pages might not have <main>, extract everything between header and footer
                body = soup.body
                if body.header:
                    body.header.decompose()
                if body.footer:
                    body.footer.decompose()
                # remove scripts
                for s in body.find_all('script'):
                    s.decompose()
                main = body
                
            fix_links(main, Path(root))
            
            main_html = "".join(str(c) for c in main.contents)
            
            # Construct Astro page
            astro_content = f"""---
import Layout from '{"../" * (len(Path(root).relative_to(OLD_DOCS).parts) + 1)}layouts/Layout.astro';
---

<Layout 
  title="{title.replace('"', '\\"')}"
  description="{description.replace('"', '\\"')}"
  canonical="{canonical}"
  hreflangs={{{repr(hreflangs)}}}
>
"""
            if head_extras:
                astro_content += '  <Fragment slot="head">\n    ' + '\n    '.join(head_extras) + '\n  </Fragment>\n'
                
            astro_content += f"\n  {main_html}\n</Layout>\n"
            
            # Write to src/pages
            rel_path = filepath.relative_to(OLD_DOCS)
            dest = PAGES_DIR / rel_path.with_suffix('.astro')
            
            if dest.name == 'index.astro':
                # it's an index page
                pass
            else:
                # optionally we could make directories for clean URLs but Astro handles .astro without .html
                # Wait, if we name it export-transcript-to-srt.astro, Astro will serve it at /export-transcript-to-srt
                pass
                
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Special case: don't write html extension in Astro
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(astro_content)

if __name__ == '__main__':
    migrate()
