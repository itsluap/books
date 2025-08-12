import os
import glob

# Get all chapter files
chapter_files = glob.glob("the_wrong_answer/chapters/chapter-*.md")

for file_path in chapter_files:
    # Read the current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has front matter
    if not content.startswith('---'):
        # Add front matter
        new_content = "---\nlayout: default\n---\n\n" + content
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added front matter to {file_path}")
    else:
        print(f"Already has front matter: {file_path}")

print("Done!")
