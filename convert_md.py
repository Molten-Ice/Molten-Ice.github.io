import markdown
import os
from pathlib import Path
import re

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .story-container {{
            max-width: 680px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        h1 {{
            text-align: center;
            font-size: 32px;
            margin-bottom: 24px;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            max-height: 400px;
            display: block;
            margin: 0 auto 32px auto;
            object-fit: cover;
        }}
        
        p {{
            font-size: 18px;
            margin-bottom: 24px;
            text-align: justify;
        }}
        
        .story-title {{
            text-align: center;
            font-size: 36px;
            margin-bottom: 32px;
            font-weight: 700;
        }}
        
        .table-of-contents {{
            background-color: #f8f8f8;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 32px;
            border: 1px solid #e1e1e1;
        }}
        
        .table-of-contents a {{
            color: #2c1810;
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        .table-of-contents a:hover {{
            color: #8b4513;
            text-decoration: none;
            border-bottom: 1px solid #8b4513;
        }}
        
        h1 {{
            text-align: center;
            font-size: 32px;
            margin-bottom: 24px;
        }}
        
        .home-header {{
            background-color: #fcfcfc;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #eee;
            margin-bottom: 20px;
        }}
        
        .home-link {{
            color: #666;
            text-decoration: none;
            font-size: 16px;
            font-weight: 400;
            transition: color 0.2s ease;
        }}
        
        .home-link:hover {{
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="home-header">
        <a href="../../index.html" class="home-link">Home</a>
    </div>
    <div class="story-container">
        <img src="../../writings/images/{image_name}.png" alt="{title}">
        {content}
    </div>
</body>
</html>
"""

def create_table_of_contents(md_content):
    # Find all chapter headings - modified to allow optional space before colon
    chapter_pattern = r'##\s*\*?\*?Chapter\s+(\d+)\s*:\s*(.*?)\*?\*?$'
    chapters = re.finditer(chapter_pattern, md_content, re.MULTILINE)
    
    toc = []
    # Keep track of replacements we need to make
    replacements = []
    
    for match in chapters:
        chapter_num = match.group(1)
        # Strip asterisks from chapter title before adding to TOC
        chapter_title = match.group(2).strip().replace('*', '')
        chapter_id = f"chapter-{chapter_num}"
        toc.append(f'<li><a href="#{chapter_id}">Chapter {chapter_num}: {chapter_title}</a></li>')
        
        # Store the original text and its replacement with an anchor
        original = match.group(0)
        replacement = f'{original}\n<a id="{chapter_id}"></a>'
        replacements.append((original, replacement))
    
    # Apply replacements to the content
    modified_content = md_content
    for original, replacement in replacements:
        modified_content = modified_content.replace(original, replacement)
    
    # Return both the TOC HTML and the modified content
    toc_html = f'''
        <div class="table-of-contents">
            <h2>Table of Contents</h2>
            <ul>
                {''.join(toc)}
            </ul>
        </div>
        ''' if toc else ''
        
    return toc_html, modified_content

def convert_md_to_html():
    output_dir = Path("writings/html")
    output_dir.mkdir(exist_ok=True)
    
    writings_dir = Path("writings")
    md_files = list(writings_dir.glob("**/*.md"))
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # Generate table of contents and get modified content
        toc_html, modified_content = create_table_of_contents(md_content)
        
        # Convert markdown to HTML using the modified content
        html_content = markdown.markdown(modified_content)
        
        # Combine TOC with content
        complete_content = toc_html + html_content
        
        title = ''.join(' ' + c if c.isupper() else c for c in md_file.stem).strip()
        
        final_html = HTML_TEMPLATE.format(
            title=title,
            image_name=md_file.stem,
            content=complete_content
        )
        
        output_path = output_dir / f"{md_file.stem}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"Converted {md_file} to {output_path}")

if __name__ == "__main__":
    convert_md_to_html()