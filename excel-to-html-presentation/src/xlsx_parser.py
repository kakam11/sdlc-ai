"""Parse an Excel workbook into a list of Slide objects.

Column convention (header row, case-insensitive): Title, Content, Image.
Each subsequent row becomes one Slide.
"""

from dataclasses import dataclass, field
from pathlib import Path

import openpyxl


@dataclass
class Slide:
    """One slide parsed from a spreadsheet row."""

    title: str
    content_lines: list[str] = field(default_factory=list)
    image_path: str | None = None


def _normalize_header(value: object) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower()


def _split_content(value: object) -> list[str]:
    if value is None:
        return []
    text = str(value)
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_workbook(path: Path) -> list[Slide]:
    """Load the first worksheet of an .xlsx file and map its rows to Slides.

    The header row's columns are matched case-insensitively against
    "Title", "Content", and "Image". Each data row below the header
    becomes one Slide, with the Content cell split on newlines into
    content_lines.
    """
    workbook = openpyxl.load_workbook(path, data_only=True)
    worksheet = workbook.worksheets[0]

    rows = worksheet.iter_rows(values_only=True)
    header_row = next(rows, None)

    column_index: dict[str, int] = {}
    if header_row is not None:
        for index, cell_value in enumerate(header_row):
            normalized = _normalize_header(cell_value)
            if normalized in ("title", "content", "image"):
                column_index[normalized] = index

    title_index = column_index.get("title")
    content_index = column_index.get("content")
    image_index = column_index.get("image")

    slides: list[Slide] = []
    for slide_number, row in enumerate(rows, start=1):
        title_value = row[title_index] if title_index is not None and title_index < len(row) else None
        content_value = row[content_index] if content_index is not None and content_index < len(row) else None
        image_value = row[image_index] if image_index is not None and image_index < len(row) else None

        title = str(title_value).strip() if title_value is not None and str(title_value).strip() else f"Slide {slide_number}"
        content_lines = _split_content(content_value)
        image_path = str(image_value).strip() if image_value is not None and str(image_value).strip() else None

        slides.append(Slide(title=title, content_lines=content_lines, image_path=image_path))

    return slides
