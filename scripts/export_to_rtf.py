"""
Export the cookbook markdown into an RTF layout tuned for Microsoft Publisher.

The RTF file preserves heading hierarchy (H1/H2/H3), bullet spacing, and
numbered steps so it can be imported into Publisher and saved as a .pub file.
"""
from __future__ import annotations

from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "Mac-and-Cheese-Cookbook.md"
DEST_DIR = PROJECT_ROOT / "publisher"
DEST = DEST_DIR / "Mac-and-Cheese-Cookbook.rtf"


def escape_rtf(text: str) -> str:
    """Escape RTF control characters."""
    return (
        text.replace("\\", r"\\")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def apply_inline_styles(text: str) -> str:
    """Convert basic markdown emphasis to RTF while escaping control chars."""
    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", text):
        if match.start() > cursor:
            parts.append(escape_rtf(text[cursor:match.start()]))
        parts.append(rf"\b {escape_rtf(match.group(1))} \b0")
        cursor = match.end()
    if cursor < len(text):
        parts.append(escape_rtf(text[cursor:]))
    return "".join(parts)


def heading(line: str, level: int) -> str:
    """Format headings with Publisher-friendly spacing and size."""
    text = apply_inline_styles(line[level + 1 :].strip())
    if level == 1:
        return rf"\pard\qc\b\f1\fs56\sa360 {text}\par"
    if level == 2:
        return rf"\pard\b\f1\fs36\sa280 {text}\par"
    return rf"\pard\b\f1\fs28\sa200 {text}\par"


def bullet(line: str) -> str:
    text = apply_inline_styles(line[2:].strip())
    return rf"\pard\fi-360\li720\sa120\f0\u8226\tab {text}\par"


def numbered(line: str) -> str:
    match = re.match(r"(\d+)\.\s+(.*)", line)
    if not match:
        return paragraph(line)
    number, content = match.groups()
    content = apply_inline_styles(content.strip())
    return rf"\pard\fi-360\li720\sa120\f0 {number}.\tab {content}\par"


def paragraph(line: str) -> str:
    text = apply_inline_styles(line.strip())
    return rf"\pard\sa160\sl276\slmult1\f0 {text}\par"


def convert_markdown(lines: list[str]) -> str:
    body: list[str] = []
    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            body.append(r"\par")
            continue
        if line.startswith("# "):
            body.append(heading(line, level=1))
        elif line.startswith("## "):
            body.append(heading(line, level=2))
        elif line.startswith("### "):
            body.append(heading(line, level=3))
        elif line.startswith("- "):
            body.append(bullet(line))
        elif re.match(r"\d+\.\s+", line):
            body.append(numbered(line))
        else:
            body.append(paragraph(line))
    body.append("}")
    return "\n".join(body)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source manuscript not found: {SOURCE}")
    DEST_DIR.mkdir(exist_ok=True)
    header = (
        r"{\rtf1\ansi\deff0"
        r"{\fonttbl{\f0 Calibri;}{\f1 Cambria;}}"
        r"\viewkind4\uc1"
        r"\margl1440\margr1440\margt1440\margb1440"
        r"\widowctrl"
    )
    manuscript = SOURCE.read_text(encoding="utf-8").splitlines()
    rtf_body = convert_markdown(manuscript)
    DEST.write_text("\n".join([header, rtf_body]), encoding="utf-8")


if __name__ == "__main__":
    main()
