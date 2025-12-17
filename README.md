# Mac and Cheese Book

This repository contains the KDP-friendly mac and cheese cookbook manuscript and supporting export assets.

## Manuscript
- Primary source: `Mac-and-Cheese-Cookbook.md` (H1 title, H2 sections, H3 recipes).
- Image prompts: `Mac-and-Cheese-Image-Prompts.md`.

## Publisher-ready export
Use the included RTF exporter to move the manuscript into Microsoft Publisher with preserved headings, bullets, and spacing.

1. Ensure you are in the repo root: `cd /workspace/Mac-and-cheese-book`.
2. Run the exporter: `python scripts/export_to_rtf.py`.
3. Import `publisher/Mac-and-Cheese-Cookbook.rtf` into Publisher (Insert > Object > Create from file), then save as `.pub`.

See `publisher/README.md` for detailed layout notes.
