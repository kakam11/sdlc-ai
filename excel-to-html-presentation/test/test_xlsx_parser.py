"""Tests for xlsx_parser.parse_workbook: happy path and edge cases/errors."""

import sys
from pathlib import Path

import openpyxl
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from xlsx_parser import (
    InvalidWorkbookError,
    MissingColumnsError,
    Slide,
    parse_workbook,
)


def _write_workbook(path: Path, header: list[str], rows: list[list[object]]) -> None:
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(header)
    for row in rows:
        worksheet.append(row)
    workbook.save(path)


@pytest.fixture
def valid_workbook(tmp_path: Path) -> Path:
    path = tmp_path / "slides.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[
            ["First Slide", "Point one\nPoint two", "images/first.png"],
            ["Second Slide", "Only point", None],
            ["Third Slide", "Alpha\nBeta\nGamma", "images/third.jpg"],
        ],
    )
    return path


def test_parses_multiple_rows_into_expected_slides(valid_workbook: Path) -> None:
    slides = parse_workbook(valid_workbook)

    assert len(slides) == 3
    assert all(isinstance(slide, Slide) for slide in slides)

    assert slides[0].title == "First Slide"
    assert slides[0].content_lines == ["Point one", "Point two"]
    assert slides[0].image_path == "images/first.png"

    assert slides[1].title == "Second Slide"
    assert slides[1].content_lines == ["Only point"]
    assert slides[1].image_path is None

    assert slides[2].title == "Third Slide"
    assert slides[2].content_lines == ["Alpha", "Beta", "Gamma"]
    assert slides[2].image_path == "images/third.jpg"


def test_header_matching_is_case_insensitive(tmp_path: Path) -> None:
    path = tmp_path / "mixed_case_headers.xlsx"
    _write_workbook(
        path,
        header=["title", "CONTENT", "ImAgE"],
        rows=[["Only Slide", "Just one line", "pic.png"]],
    )

    slides = parse_workbook(path)

    assert len(slides) == 1
    assert slides[0].title == "Only Slide"
    assert slides[0].content_lines == ["Just one line"]
    assert slides[0].image_path == "pic.png"


def test_multiline_content_splits_into_content_lines(tmp_path: Path) -> None:
    path = tmp_path / "multiline.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[["Bulleted Slide", "Line one\nLine two\nLine three\n", None]],
    )

    slides = parse_workbook(path)

    assert len(slides) == 1
    assert slides[0].content_lines == ["Line one", "Line two", "Line three"]


def test_multiline_content_drops_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "multiline_blanks.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[["Slide", "Line one\n\nLine two\n\n", None]],
    )

    slides = parse_workbook(path)

    assert slides[0].content_lines == ["Line one", "Line two"]


def test_missing_title_column_raises_missing_columns_error(tmp_path: Path) -> None:
    path = tmp_path / "no_title_column.xlsx"
    _write_workbook(
        path,
        header=["Content", "Image"],
        rows=[["Some content", None]],
    )

    with pytest.raises(MissingColumnsError) as exc_info:
        parse_workbook(path)

    message = str(exc_info.value)
    assert "Title" in message
    assert "Content" in message


def test_missing_content_column_raises_missing_columns_error(tmp_path: Path) -> None:
    path = tmp_path / "no_content_column.xlsx"
    _write_workbook(
        path,
        header=["Title", "Image"],
        rows=[["Some title", None]],
    )

    with pytest.raises(MissingColumnsError) as exc_info:
        parse_workbook(path)

    message = str(exc_info.value)
    assert "Title" in message
    assert "Content" in message


def test_missing_both_required_columns_raises_missing_columns_error(
    tmp_path: Path,
) -> None:
    path = tmp_path / "no_required_columns.xlsx"
    _write_workbook(
        path,
        header=["Foo", "Bar"],
        rows=[["a", "b"]],
    )

    with pytest.raises(MissingColumnsError):
        parse_workbook(path)


def test_corrupt_file_raises_invalid_workbook_error(tmp_path: Path) -> None:
    path = tmp_path / "corrupt.xlsx"
    path.write_bytes(b"this is not a real xlsx file")

    with pytest.raises(InvalidWorkbookError):
        parse_workbook(path)


def test_nonexistent_file_raises_invalid_workbook_error(tmp_path: Path) -> None:
    path = tmp_path / "does_not_exist.xlsx"

    with pytest.raises(InvalidWorkbookError):
        parse_workbook(path)


def test_zero_data_rows_returns_empty_list(tmp_path: Path) -> None:
    path = tmp_path / "header_only.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[],
    )

    slides = parse_workbook(path)

    assert slides == []


def test_blank_title_defaults_to_slide_number(tmp_path: Path) -> None:
    path = tmp_path / "blank_title.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[
            [None, "First content", None],
            ["", "Second content", None],
            ["   ", "Third content", None],
        ],
    )

    slides = parse_workbook(path)

    assert len(slides) == 3
    assert slides[0].title == "Slide 1"
    assert slides[1].title == "Slide 2"
    assert slides[2].title == "Slide 3"


def test_blank_image_stays_none(tmp_path: Path) -> None:
    path = tmp_path / "blank_image.xlsx"
    _write_workbook(
        path,
        header=["Title", "Content", "Image"],
        rows=[
            ["Slide With No Image", "Some content", None],
            ["Another Slide", "More content", ""],
            ["Whitespace Image", "Even more content", "   "],
        ],
    )

    slides = parse_workbook(path)

    assert len(slides) == 3
    assert slides[0].image_path is None
    assert slides[1].image_path is None
    assert slides[2].image_path is None
