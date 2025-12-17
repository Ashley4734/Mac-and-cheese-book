## Microsoft Publisher export

This folder contains the RTF export generated from the primary manuscript for Microsoft Publisher.

- **Source:** `Mac-and-Cheese-Cookbook.md`
- **Generated file:** `Mac-and-Cheese-Cookbook.rtf`
- **8x10 PDF:** `Mac-and-Cheese-Cookbook-8x10.pdf`
- **Generator:** `scripts/export_to_rtf.py`
- **Styles:** Title (centered), section headings (H2), recipe headings (H3), bullets for ingredient lists, and indented numbered directions. Spacing uses generous paragraph separation for clean text frames in Publisher.

### How to refresh the Publisher import
1. Ensure you are in the repository root: `cd /workspace/Mac-and-cheese-book`.
2. Run the export script: `python scripts/export_to_rtf.py`.
3. Open Microsoft Publisher and create a new blank document.
4. Insert the RTF via **Insert > Object > Create from file** or paste into a text frame; apply your preferred master page or grid.
5. Save the document as a `.pub` file for further layout adjustments.

### 8x10 PDF layout
If you need a ready-to-print PDF without Publisher, run `python scripts/export_to_pdf.py` (requires `reportlab`) from the repo root. The output is sized for an 8x10-inch trim with balanced margins and the existing heading hierarchy.

> Note: Direct `.pub` creation is not available in this environment, so the RTF export is structured to import cleanly into Publisher with minimal restyling.
