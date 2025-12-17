"""
Export the cookbook markdown into an 8x10 PDF layout tuned for KDP-ready pages.

The PDF keeps the existing heading hierarchy (H1/H2/H3), ingredient bullets,
and numbered directions while applying print-friendly spacing that fits an
8x10-inch trim size.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import re

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "Mac-and-Cheese-Cookbook.md"
DEST_DIR = PROJECT_ROOT / "publisher"
DEST = DEST_DIR / "Mac-and-Cheese-Cookbook-8x10.pdf"

PAGE_WIDTH = 8 * inch
PAGE_HEIGHT = 10 * inch
MARGIN = 0.75 * inch


def inline_format(text: str) -> str:
    """Convert basic markdown emphasis to ReportLab-safe inline tags."""

    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", text):
        if match.start() > cursor:
            parts.append(escape(text[cursor : match.start()]))
        parts.append(f"<b>{escape(match.group(1))}</b>")
        cursor = match.end()
    if cursor < len(text):
        parts.append(escape(text[cursor:]))
    return "".join(parts)


def build_styles() -> StyleSheet1:
    styles = StyleSheet1()
    styles.add(
        ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            "Heading2",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "Heading3",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "List",
            parent=styles["Body"],
            leftIndent=16,
            firstLineIndent=-8,
            spaceAfter=4,
        )
    )
    return styles


def flush_list(
    flowables: list,
    items: list[str],
    styles: StyleSheet1,
    list_type: str | None,
) -> None:
    if not items:
        return

    bullet_type = "1" if list_type == "numbered" else "bullet"
    bullet_flowable = ListFlowable(
        [ListItem(Paragraph(inline_format(text), styles["List"])) for text in items],
        bulletType=bullet_type,
        start="1" if list_type == "numbered" else None,
        leftIndent=12,
        bulletFontName="Helvetica",
        bulletFontSize=10,
    )
    bullet_flowable.spaceBefore = 2
    bullet_flowable.spaceAfter = 8
    flowables.append(bullet_flowable)
    items.clear()


def convert_markdown(lines: list[str], styles: StyleSheet1) -> list:
    story: list = []
    list_items: list[str] = []
    list_type: str | None = None

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if not stripped:
            flush_list(story, list_items, styles, list_type)
            list_type = None
            story.append(Spacer(1, 6))
            continue

        if line.startswith("# "):
            flush_list(story, list_items, styles, list_type)
            list_type = None
            story.append(Paragraph(inline_format(line[2:].strip()), styles["Title"]))
        elif line.startswith("## "):
            flush_list(story, list_items, styles, list_type)
            list_type = None
            story.append(Paragraph(inline_format(line[3:].strip()), styles["Heading2"]))
        elif line.startswith("### "):
            flush_list(story, list_items, styles, list_type)
            list_type = None
            story.append(Paragraph(inline_format(line[4:].strip()), styles["Heading3"]))
        elif line.startswith("- "):
            if list_type not in {"bullet", None}:
                flush_list(story, list_items, styles, list_type)
                list_items = []
            list_type = "bullet"
            list_items.append(line[2:].strip())
        elif re.match(r"\d+\.\s+", line):
            if list_type not in {"numbered", None}:
                flush_list(story, list_items, styles, list_type)
                list_items = []
            list_type = "numbered"
            list_items.append(re.sub(r"^\d+\.\s+", "", line).strip())
        else:
            flush_list(story, list_items, styles, list_type)
            list_type = None
            story.append(Paragraph(inline_format(line), styles["Body"]))

    flush_list(story, list_items, styles, list_type)
    return story


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source manuscript not found: {SOURCE}")

    DEST_DIR.mkdir(exist_ok=True)
    styles = build_styles()
    manuscript_lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = convert_markdown(manuscript_lines, styles)

    doc = SimpleDocTemplate(
        str(DEST),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="Mac and Cheese Cookbook",
    )
    doc.build(story)


if __name__ == "__main__":
    main()
