"""
Build script for AI Security Architecture Guide.
Produces a single PDF from Markdown source files.

Usage:
    python build.py              # Build PDF
    python build.py --html       # Also save intermediate HTML

Requirements:
    pip install markdown playwright
    playwright install chromium
"""

import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

# --- Configuration ---

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
EXERCISES_DIR = BASE_DIR / "exercises"
STYLE_FILE = BASE_DIR / "style.css"
OUTPUT_DIR = BASE_DIR / "export"

PDF_FILE = OUTPUT_DIR / "AI-Security-Architecture-Guide.pdf"
HTML_FILE = OUTPUT_DIR / "AI-Security-Architecture-Guide.html"

# Content chapters (in order)
CHAPTERS = [
    "chapter-01-ai-landscape.md",
    "chapter-02-how-llms-work.md",
    "chapter-03-threat-modeling.md",
    "chapter-04-prompt-injection.md",
    "chapter-05-jailbreaks-guardrail-bypass.md",
    "chapter-06-data-leakage-privacy.md",
    "chapter-07-secure-ai-design.md",
    "chapter-08-supply-chain-security.md",
    "chapter-09-reference-architectures.md",
    "chapter-10-ai-security-program.md",
    "appendix-a-cheat-sheet.md",
    "appendix-b-tools-resources.md",
    "appendix-c-glossary.md",
]

# Exercise files
EXERCISES = [
    "exercise-01-threat-model-chatbot.md",
    "exercise-02-prompt-injection-lab.md",
    "exercise-03-design-review.md",
    "exercise-04-supply-chain-audit.md",
    "exercise-05-architecture-challenge.md",
]

# --- Cover Page ---

COVER = """
<div class="cover-page">
    <h1>AI Security Architecture</h1>
    <div class="subtitle">A Practical Guide to Securing LLM-Powered Systems</div>
    <div class="edition">Threat Modeling &bull; Secure Design &bull; Reference Architectures &bull; 2026 Edition</div>
    <div class="tagline">
        10 chapters &bull; 5 hands-on exercises &bull; No AI/ML experience required
    </div>
</div>
"""

# --- TOC ---

TOC_ENTRIES = [
    ("Chapter 1: The AI Security Landscape", True),
    ("Chapter 2: How LLMs Work (Just Enough to Secure Them)", True),
    ("Chapter 3: Threat Modeling AI Systems", True),
    ("Chapter 4: Prompt Injection", True),
    ("Chapter 5: Jailbreaks & Guardrail Bypass", True),
    ("Chapter 6: Data Leakage & Privacy", True),
    ("Chapter 7: Secure AI System Design", True),
    ("Chapter 8: AI Supply Chain Security", True),
    ("Chapter 9: Reference Architectures", True),
    ("Chapter 10: Building Your AI Security Program", True),
    ("Appendix A: AI Security Cheat Sheet", False),
    ("Appendix B: Tools & Resources", False),
    ("Appendix C: Glossary", False),
    ("Exercises", False),
]


def build_toc(entries):
    items = []
    for title, is_chapter in entries:
        css_class = "chapter-entry" if is_chapter else "appendix-entry"
        items.append(f'<li class="{css_class}">{title}</li>')
    return f"""
<div class="toc">
    <h1>Table of Contents</h1>
    <ul>
        {"".join(items)}
    </ul>
</div>
"""


def md_to_html(source_dir, filenames):
    """Convert markdown files to HTML sections."""
    md_extensions = ["tables", "fenced_code"]
    sections = []

    for filename in filenames:
        filepath = source_dir / filename
        if not filepath.exists():
            print(f"  WARNING: {filename} not found, skipping.")
            continue

        md_text = filepath.read_text(encoding="utf-8")
        html = markdown.markdown(md_text, extensions=md_extensions)
        # Convert markdown checkboxes to HTML
        html = html.replace("[ ]", '<input type="checkbox" disabled>')
        html = html.replace("[x]", '<input type="checkbox" checked disabled>')
        sections.append(f'<div class="chapter">\n{html}\n</div>')

    return sections


def build_document():
    """Build the complete HTML document."""
    css = STYLE_FILE.read_text(encoding="utf-8")

    # Build chapter content
    chapter_sections = md_to_html(CONTENT_DIR, CHAPTERS)
    print(f"  Loaded {len(chapter_sections)} chapters.")

    # Build exercise content
    exercise_sections = md_to_html(EXERCISES_DIR, EXERCISES)
    print(f"  Loaded {len(exercise_sections)} exercises.")

    all_sections = chapter_sections + exercise_sections

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
{css}
    </style>
</head>
<body>
{COVER}
{build_toc(TOC_ENTRIES)}
{"".join(all_sections)}
</body>
</html>"""


def render_pdf(html_content, html_path, pdf_path):
    """Render HTML to PDF using Playwright Chromium."""
    html_path.write_text(html_content, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{html_path.resolve().as_posix()}")
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=str(pdf_path),
            format="Letter",
            margin={
                "top": "0.85in",
                "bottom": "0.85in",
                "left": "0.85in",
                "right": "0.85in",
            },
            print_background=True,
            display_header_footer=True,
            header_template="<span></span>",
            footer_template="""
                <div style="font-size: 9px; color: #666; width: 100%; text-align: center;">
                    <span class="pageNumber"></span>
                </div>
            """,
        )
        browser.close()

    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"  PDF saved: {pdf_path} ({size_mb:.1f} MB)")


def main():
    save_html = "--html" in sys.argv

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Building AI Security Architecture Guide...")
    html = build_document()
    render_pdf(html, HTML_FILE, PDF_FILE)
    if not save_html:
        HTML_FILE.unlink(missing_ok=True)

    print("\nDone.")


if __name__ == "__main__":
    main()
