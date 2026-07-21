# Design: Excel to HTML Presentation

## Overview
A Python desktop app using Tkinter (stdlib, already available in this workspace's `.venv` — no new GUI dependency) for the file-picker/generate UI, and `openpyxl` (needs installing into the existing `.venv`) to read `.xlsx` files. Parsing and HTML generation are kept as plain functions separate from the GUI, so they're unit-testable without driving Tkinter. The generated HTML embeds everything (CSS, JS, images-as-base64) in one file, with a small vanilla-JS slide deck (no external libraries) handling navigation.

## Architecture
```
excel-to-html-presentation/
  src/
    main.py            # entry point: launches the GUI
    gui.py              # Tkinter App: file picker, generate button, status messages
    xlsx_parser.py       # Slide model + parse_workbook()
    html_generator.py    # generate_html() + image embedding
  test/
    test_xlsx_parser.py
    test_html_generator.py
```
Flow: GUI "Choose File" → `parse_workbook()` → GUI shows slide count → "Generate" → `generate_html()` → GUI writes output (via a temp-file-then-rename) → success/warning message.

## Components & Interfaces

**`Slide` (dataclass, in `xlsx_parser.py`)**
- `title: str`, `content_lines: list[str]`, `image_path: str | None`
- Plain data holder passed between parsing and generation.

**`parse_workbook(path: Path) -> list[Slide]`** (`xlsx_parser.py`)
- Loads the first worksheet with `openpyxl.load_workbook`. Wraps load errors (bad/corrupt file) in a single `InvalidWorkbookError`.
- Matches header row columns case-insensitively for `Title`, `Content`, `Image`; raises `MissingColumnsError` (with the expected layout in its message) if `Title` or `Content` is absent.
- Returns `[]` if there are no data rows — caller decides how to present that.
- Per row: `title` falls back to `f"Slide {row_number}"` if blank; `content_lines` is the `Content` cell split on newlines with blank lines dropped; `image_path` is the `Image` cell value or `None` if blank.
- Satisfies Requirement 1.2, 1.3 (via `InvalidWorkbookError`), 1.4, 2.1, 2.2, 2.3, 2.4, 2.5.

**`resolve_image(image_path: str | None, base_dir: Path) -> str | None`** (`html_generator.py`)
- Resolves a relative `image_path` against `base_dir` (the spreadsheet's own directory), reads it, and returns a `data:` URI (`base64`, mime type from the file extension). Returns `None` if `image_path` is `None` or the file can't be read — never raises.
- Satisfies Requirement 3.2, 3.3.

**`generate_html(slides: list[Slide], base_dir: Path) -> tuple[str, list[str]]`** (`html_generator.py`)
- Builds one HTML document: an inline `<style>` block for slide layout, one `<section class="slide">` per slide (title, a `<ul>` of `content_lines`, an optional `<img>` from `resolve_image`), and an inline `<script>` implementing show-one-slide-at-a-time navigation (next/previous buttons, left/right arrow key listeners, an `N / total` counter).
- Returns `(html_string, warnings)` where `warnings` lists which slides (by title) had an unresolved image, for Requirement 3.3.
- Satisfies Requirement 3.1, 3.2, 3.3, 3.4.

**`App` (Tkinter, in `gui.py`)**
- "Choose File" button → `filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])` → calls `parse_workbook`; on success shows "`N` slides found" and enables "Generate"; on `InvalidWorkbookError`/`MissingColumnsError` shows the error message and leaves "Generate" disabled; on zero slides shows "No slides found in this file" and leaves "Generate" disabled.
- "Generate" button (disabled until a valid load) → `filedialog.asksaveasfilename(defaultextension=".html", initialfile=<spreadsheet-stem>.html)` → calls `generate_html`, writes to `<target>.tmp` then `os.replace()`s it onto the target path (so a failed write never leaves a partial file at the destination), then shows a success message with the output path plus any image warnings.
- Satisfies Requirement 1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3, 4.4.

**`main.py`**
- Instantiates and runs `App`. No logic of its own.

## Data Models
`Slide` is the only data model (see above) — no persistence, the app is stateless between runs.

## Error Handling
- Corrupt/invalid `.xlsx` → `InvalidWorkbookError` from `parse_workbook` → GUI error label, no crash (1.3).
- Zero data rows → `parse_workbook` returns `[]` → GUI shows "no slides" message, Generate stays disabled (1.4).
- Missing `Title`/`Content` header columns → `MissingColumnsError` with the expected column layout in its message → GUI error label (2.5).
- Missing `Title` cell on a row → defaulted to `Slide N`, generation continues (2.3).
- Blank `Image` cell → slide rendered without an image, no warning (2.4).
- Unreadable/missing image file → `resolve_image` returns `None`, slide still generates, its title is added to the `warnings` list shown after generation (3.3).
- Output write failure (permissions, disk full) → writing to a `.tmp` path first means a failed write never corrupts/half-writes the target; the `.tmp` file is removed and a clear error is shown (4.4).

## Testing Strategy
- Unit tests (`pytest`) for `parse_workbook` against small `.xlsx` fixtures built with `openpyxl` in test setup: valid file, missing header columns, blank titles, blank images, zero data rows — covers Requirement 1 and 2.
- Unit tests for `generate_html`/`resolve_image`: single- and multi-slide output contains expected titles/content, a valid image path embeds a `data:` URI, a bad image path yields `None` plus a warning entry, output contains no external `http`/relative asset references — covers Requirement 3.
- Tkinter GUI wiring (`gui.py`) is exercised with a manual smoke test per task (launch the app, pick a real file, generate, open the resulting HTML in a browser) rather than automated GUI tests, since driving Tkinter interactions programmatically adds little value for an app this size — covers Requirement 1 and 4 end-to-end.

---
**Status:** Approved
