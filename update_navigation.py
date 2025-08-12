import os
import re
from typing import List, Tuple, Optional


NAV_START = "<!-- NAVIGATION START -->"
NAV_END = "<!-- NAVIGATION END -->"


def find_book_dirs(root: str) -> List[str]:
    book_dirs: List[str] = []
    for entry in os.listdir(root):
        full = os.path.join(root, entry)
        if not os.path.isdir(full):
            continue
        if os.path.exists(os.path.join(full, "SUMMARY.md")) and os.path.exists(
            os.path.join(full, "book.toml")
        ):
            book_dirs.append(full)
    return sorted(book_dirs)


def parse_summary(summary_path: str) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    with open(summary_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Match list items like: - [Title](path/to/file.md)
            m = re.match(r"^- \[(?P<title>[^\]]+)\]\((?P<path>[^\)]+)\)", line)
            if not m:
                continue
            title = m.group("title").strip()
            rel_path = m.group("path").strip()
            if not rel_path.lower().endswith(".md"):
                continue
            items.append((title, rel_path))
    return items


def compute_relative_html(from_md: str, to_md: str) -> str:
    """Compute a relative .html href from one markdown file to another."""
    from_dir = os.path.dirname(from_md)
    target_html = os.path.splitext(to_md)[0] + ".html"
    rel = os.path.relpath(target_html, start=from_dir or ".")
    # Normalize Windows backslashes to URL slashes
    return rel.replace(os.sep, "/")


def toc_href(from_md: str, book_dir: str) -> str:
    from_dir = os.path.dirname(from_md)
    # Link to the book index.html
    target = os.path.join(book_dir, "index.html")
    rel = os.path.relpath(target, start=from_dir or ".")
    return rel.replace(os.sep, "/")


def build_nav_html(
    current_md: str,
    book_dir: str,
    prev_item: Optional[Tuple[str, str]],
    next_item: Optional[Tuple[str, str]],
) -> str:
    parts: List[str] = []
    parts.append(NAV_START)
    parts.append(
        '<div style="border-top: 1px solid #e1e4e8; margin-top: 40px; padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">'
    )

    # Prev
    if prev_item:
        prev_title, prev_path = prev_item
        href = compute_relative_html(current_md, os.path.join(book_dir, prev_path))
        parts.append(
            f'  <a href="{href}" style="background-color: #f1f8ff; border: 1px solid #c8e1ff; padding: 8px 16px; text-decoration: none; border-radius: 6px;">← {prev_title}</a>'
        )
    else:
        parts.append("  <div></div>")

    # TOC
    parts.append(
        f'  <a href="{toc_href(current_md, book_dir)}" style="background-color: #f6f8fa; border: 1px solid #d1d9e0; padding: 8px 16px; text-decoration: none; border-radius: 6px;">📚 Table of Contents</a>'
    )

    # Next
    if next_item:
        next_title, next_path = next_item
        href = compute_relative_html(current_md, os.path.join(book_dir, next_path))
        parts.append(
            f'  <a href="{href}" style="background-color: #f1f8ff; border: 1px solid #c8e1ff; padding: 8px 16px; text-decoration: none; border-radius: 6px;">{next_title} →</a>'
        )
    else:
        parts.append("  <div></div>")

    parts.append("</div>")
    parts.append(NAV_END)
    parts.append("")
    return "\n".join(parts)


def strip_existing_nav(content: str) -> str:
    return re.sub(
        re.compile(rf"{re.escape(NAV_START)}[\s\S]*?{re.escape(NAV_END)}\s*", re.MULTILINE),
        "",
        content,
    )


def update_book_navigation(book_dir: str) -> None:
    summary_path = os.path.join(book_dir, "SUMMARY.md")
    if not os.path.exists(summary_path):
        print(f"No SUMMARY.md in {book_dir}, skipping")
        return

    items = parse_summary(summary_path)
    if not items:
        print(f"No chapter items found in {summary_path}, skipping")
        return

    # Convert relative paths to absolute md paths for editing
    abs_items: List[Tuple[str, str]] = []
    for title, rel_path in items:
        abs_md = os.path.normpath(os.path.join(book_dir, rel_path))
        if not os.path.exists(abs_md):
            print(f"Missing file listed in SUMMARY: {abs_md}")
            continue
        abs_items.append((title, abs_md))

    for i, (title, abs_md) in enumerate(abs_items):
        prev_item = (
            (abs_items[i - 1][0], os.path.relpath(abs_items[i - 1][1], book_dir))
            if i > 0
            else None
        )
        next_item = (
            (abs_items[i + 1][0], os.path.relpath(abs_items[i + 1][1], book_dir))
            if i < len(abs_items) - 1
            else None
        )

        with open(abs_md, "r", encoding="utf-8") as f:
            content = f.read()

        content = strip_existing_nav(content).rstrip() + "\n\n" + build_nav_html(
            abs_md, book_dir, prev_item, next_item
        )

        with open(abs_md, "w", encoding="utf-8") as f:
            f.write(content)

        rel = os.path.relpath(abs_md, book_dir)
        print(f"Added navigation to {book_dir}/{rel}")


def main():
    root = os.getcwd()
    books = find_book_dirs(root)
    if not books:
        print("No books found (directories with SUMMARY.md and book.toml)")
        return
    for book in books:
        print(f"Processing {book}...")
        update_book_navigation(book)
    print("Done! Navigation added to all books.")


if __name__ == "__main__":
    main()


