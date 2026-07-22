"""Tests for xlsx_parser.parse_workbook happy-path parsing."""

import sys
from pathlib import Path

import openpyxl
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from xlsx_parser import Slide, parse_workbook


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
