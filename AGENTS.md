# Agent Instructions

- This repository contains the Mac and Cheese cookbook content intended for KDP-friendly export (print-ready PDF and EPUB). Maintain consistent heading hierarchy and recipe numbering.
- Keep the primary manuscript in Markdown with clear section breaks, using H1/H2/H3 for title, sections, and recipes respectively.
- Recipe entries should include servings, time, ingredients, and steps; keep directions concise for print layout.
- Keep image prompts in a separate file aligned to recipe numbering.
- When updating content, preserve at least 100 distinct recipes and maintain the numbering scheme.
- Publisher-ready exports should be generated via `python scripts/export_to_rtf.py` (RTF importable into Microsoft Publisher); direct `.pub` creation is not available in this environment due to restricted package downloads.
- For print-ready output without Publisher, use `python scripts/export_to_pdf.py` to create an 8x10-inch PDF in `publisher/` (requires `reportlab`).
