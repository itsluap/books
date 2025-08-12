import os
import re

# Define the chapter order
chapters = [
    ("front-matter.md", "Front Matter"),
    ("chapters/chapter-01-the-perfect-lesson.md", "Chapter 1 — The Perfect Lesson"),
    ("chapters/chapter-02-system-flags.md", "Chapter 2 — System Flags"),
    ("chapters/chapter-03-home-compliance.md", "Chapter 3 — Home Compliance"),
    ("chapters/chapter-04-the-forgotten-library.md", "Chapter 4 — The Forgotten Library"),
    ("chapters/chapter-05-the-watchers.md", "Chapter 5 — The Watchers"),
    ("chapters/chapter-06-the-first-broadcast.md", "Chapter 6 — The First Broadcast"),
    ("chapters/chapter-07-the-ministry-responds.md", "Chapter 7 — The Ministry Responds"),
    ("chapters/chapter-08-code-in-the-cracks.md", "Chapter 8 — Code in the Cracks"),
    ("chapters/chapter-09-operation-contradiction.md", "Chapter 9 — Operation Contradiction"),
    ("chapters/chapter-10-capture.md", "Chapter 10 — Capture"),
    ("chapters/chapter-11-the-core.md", "Chapter 11 — The Core"),
    ("chapters/chapter-12-the-wrong-answer-that-saved-the-world.md", "Chapter 12 — The Wrong Answer That Saved the World")
]

def add_navigation(file_path, title, prev_link=None, next_link=None):
    full_path = f"the_wrong_answer/{file_path}"
    
    # Read current content
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create navigation HTML
    nav_html = '\n<div style="border-top: 1px solid #e1e4e8; margin-top: 40px; padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">\n'
    
    if prev_link:
        nav_html += f'  <a href="{prev_link[0]}" style="background-color: #f1f8ff; border: 1px solid #c8e1ff; padding: 8px 16px; text-decoration: none; border-radius: 6px;">← {prev_link[1]}</a>\n'
    else:
        nav_html += '  <div></div>\n'
    
    nav_html += '  <a href="../" style="background-color: #f6f8fa; border: 1px solid #d1d9e0; padding: 8px 16px; text-decoration: none; border-radius: 6px;">📚 Table of Contents</a>\n'
    
    if next_link:
        nav_html += f'  <a href="{next_link[0]}" style="background-color: #f1f8ff; border: 1px solid #c8e1ff; padding: 8px 16px; text-decoration: none; border-radius: 6px;">{next_link[1]} →</a>\n'
    else:
        nav_html += '  <div></div>\n'
    
    nav_html += '</div>\n'
    
    # Remove existing navigation if present
    content = re.sub(r'<div style="border-top.*?</div>\s*$', '', content, flags=re.DOTALL)
    
    # Add new navigation
    content = content.rstrip() + nav_html
    
    # Write back
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added navigation to {file_path}")

# Add navigation to each chapter
for i, (file_path, title) in enumerate(chapters):
    prev_link = chapters[i-1] if i > 0 else None
    next_link = chapters[i+1] if i < len(chapters)-1 else None
    
    add_navigation(file_path, title, prev_link, next_link)

print("Done! Navigation added to all chapters.")
