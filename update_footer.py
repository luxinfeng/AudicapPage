import os
import glob
import re

def update_footer():
    docs_dir = '/Users/xinfeng/WebstormProjects/AudicapPage/docs'
    html_files = glob.glob(os.path.join(docs_dir, '**/*.html'), recursive=True)
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine relative depth
        rel_path = os.path.relpath(file_path, docs_dir)
        depth = rel_path.count(os.sep)
        
        prefix = '../' * depth if depth > 0 else ''
        
        new_links = f'''<a href="{prefix}blog/transcribe-udemy-coursera-courses.html">Transcribe Courses</a><a href="{prefix}blog/transcribe-microsoft-teams-web.html">Transcribe Teams</a><a href="{prefix}blog/summarize-long-youtube-videos.html">Summarize YouTube</a><a href="{prefix}alternatives/fireflies-ai.html">Fireflies Alternative</a><a href="{prefix}alternatives/fathom.html">Fathom Alternative</a>'''
        
        # Check if already added
        if 'Transcribe Courses' in content:
            continue
            
        # We find <div class="footer-links">...</div> and inject before the closing div
        pattern = r'(<div class="footer-links">.*?)(</div>)'
        
        new_content = re.sub(pattern, r'\1' + new_links + r'\2', content, flags=re.DOTALL)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated footer in {rel_path}")

if __name__ == '__main__':
    update_footer()
