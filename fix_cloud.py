import re
import glob

# Remove the old tag cloud from the footer
files = glob.glob('*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The tag cloud was:
    # <div class='seo-tags' style='margin-top: 20px; font-size: 0.75em; color: rgba(255,255,255,0.5); text-align: left; line-height: 1.4;'>
    # ...
    # </div></div>
    
    content = re.sub(r"<div class='seo-tags'.*?</div></div>", "", content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Tag Cloud removed from footer.")
