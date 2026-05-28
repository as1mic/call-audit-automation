import openpyxl

from pathlib import Path
from datetime import datetime


def load_report(report_path: Path):
    workbook = openpyxl.load_workbook(report_path)

    return workbook


def save_report(workbook, destination_path: Path) -> Path:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(destination_path)
    return destination_path


def get_main_sheet(workbook):
    return workbook.worksheets[0]


def find_row_by_date(sheet, target_date) -> int:
    for row in range(3, sheet.max_row + 1):
        cell_value = sheet.cell(row=row, column=1).value

        if isinstance(cell_value, datetime):
            cell_value = cell_value.strftime("%Y-%m-%d")

        if str(cell_value) == str(target_date):
            return row

    return -1
