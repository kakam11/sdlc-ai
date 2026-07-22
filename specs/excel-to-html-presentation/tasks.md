# Tasks: Excel to HTML Presentation

- [x] 1. Scaffold project and implement happy-path spreadsheet parsing
  - Create `excel-to-html-presentation/src/{xlsx_parser.py,html_generator.py,gui.py,main.py}` and `excel-to-html-presentation/test/`.
  - Install `openpyxl` into the existing `.venv`.
  - Implement the `Slide` dataclass (`title`, `content_lines`, `image_path`) in `xlsx_parser.py`.
  - Implement `parse_workbook(path)` for the happy path: load the first worksheet, match `Title`/`Content`/`Image` header columns case-insensitively, map each data row to a `Slide` (split `Content` on newlines into `content_lines`).
  - Add tests: a valid `.xlsx` fixture (built with `openpyxl` in test setup) with multiple rows parses into the expected `Slide` list; multi-line `Content` cells split correctly.
  - _Requirements: 2.1, 2.2_

- [ ] 2. Handle spreadsheet parsing edge cases and errors
  - Extend `parse_workbook`: raise `MissingColumnsError` (message names the expected `Title`/`Content`/`Image` layout) if `Title` or `Content` header is absent; wrap `openpyxl` load failures in `InvalidWorkbookError`; return `[]` for a worksheet with no data rows; default a blank `Title` cell to `f"Slide {n}"`; leave `image_path` as `None` for a blank `Image` cell.
  - Add tests for each: missing header columns, corrupt/invalid file, zero data rows, blank title, blank image.
  - _Requirements: 1.3, 1.4, 2.3, 2.4, 2.5_

- [ ] 3. Implement image resolution and base64 embedding
  - Implement `resolve_image(image_path, base_dir)` in `html_generator.py`: resolves a relative path against `base_dir`, returns a `data:` URI (base64, mime type from extension) for a readable image, and returns `None` (never raises) if `image_path` is `None` or the file can't be read.
  - Add tests: valid image file produces a `data:` URI with the right mime type; `None` path returns `None`; a nonexistent path returns `None`.
  - _Requirements: 3.2, 3.3_

- [ ] 4. Implement HTML presentation generation
  - Implement `generate_html(slides, base_dir)` in `html_generator.py`: builds one HTML document with inline `<style>`, one `<section class="slide">` per slide (title, `content_lines` as a bullet list, optional `<img>` via `resolve_image`), and an inline `<script>` for next/previous navigation, left/right arrow key handling, and an `N / total` slide counter. Returns `(html_string, warnings)` where `warnings` lists titles of slides with an unresolved image.
  - Add tests: single- and multi-slide output contains expected titles/content; a slide with a valid image embeds a `data:` URI; a slide with a bad image path produces `None` for the image and an entry in `warnings`; generated output contains no external `http`/relative asset references.
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 5. Build the GUI's file-loading flow
  - Implement the Tkinter `App` in `gui.py`: a "Choose File" button using `askopenfilename` filtered to `.xlsx`; on selection, call `parse_workbook` and show either an error label (`InvalidWorkbookError`/`MissingColumnsError`), a "no slides found" message (empty list), or a "`N` slides found" label; a "Generate" button that starts disabled and becomes enabled only after a valid non-empty load.
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1_

- [ ] 6. Build the GUI's generation flow
  - Wire the "Generate" button: `asksaveasfilename` defaulting to `<spreadsheet-stem>.html`; call `generate_html`; write output to a `<target>.tmp` path then `os.replace()` it onto the target so a failed write never leaves a partial file; show a success message with the output path plus any image warnings, or a clear error message on write failure (with the `.tmp` file cleaned up).
  - _Requirements: 4.2, 4.3, 4.4_

- [ ] 7. Wire up the entry point and verify end-to-end
  - Implement `main.py` to instantiate and run `App`.
  - Manually verify end-to-end: build a small real `.xlsx` sample (with a header row, a few slides, and at least one embedded image), launch the app, load it, generate the HTML, and open the result in a browser to confirm slide content, image embedding, and next/previous/arrow-key navigation all work.
  - _Requirements: 1.1, 1.2, 4.1, 4.2, 4.3_

---
**Status:** Approved
