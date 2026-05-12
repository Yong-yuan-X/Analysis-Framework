from __future__ import annotations

import csv
import json
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

from analysis_framework.exceptions import PipelineError


def _validate_rows(rows: object, source_path: Path) -> list[dict]:
    if not isinstance(rows, list):
        raise PipelineError(f"Input data must be a JSON array of objects: {source_path}")

    if not rows:
        raise PipelineError(f"Input file has no data rows: {source_path}")

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise PipelineError(f"Input row #{index} must be an object: {source_path}")

    if not rows[0]:
        raise PipelineError(f"Input file is missing a valid header row: {source_path}")

    return rows


def read_csv(path: str) -> list[dict]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise PipelineError(f"Input file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    return _validate_rows(rows, csv_path)


def read_json(path: str) -> list[dict]:
    json_path = Path(path)
    if not json_path.exists():
        raise PipelineError(f"Input file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict):
        payload = payload.get("data", payload.get("rows"))

    return _validate_rows(payload, json_path)


def _xlsx_column_index(cell_reference: str) -> int:
    column_name = "".join(character for character in cell_reference if character.isalpha())
    index = 0
    for character in column_name:
        index = index * 26 + ord(character.upper()) - ord("A") + 1
    return index - 1


def _xlsx_text(element: ET.Element, namespace: dict[str, str]) -> str:
    return "".join(text.text or "" for text in element.findall(".//main:t", namespace))


def _load_xlsx_shared_strings(workbook: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return []

    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    return [_xlsx_text(item, namespace) for item in root.findall("main:si", namespace)]


def _xlsx_sheet_path(workbook: zipfile.ZipFile, sheet_name: str | None) -> str:
    namespace = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
    sheets = workbook_root.findall("main:sheets/main:sheet", namespace)
    if not sheets:
        raise PipelineError("XLSX workbook does not contain any sheets.")

    selected_sheet = None
    if sheet_name is None:
        selected_sheet = sheets[0]
    else:
        for sheet in sheets:
            if sheet.get("name") == sheet_name:
                selected_sheet = sheet
                break

    if selected_sheet is None:
        available = ", ".join(sheet.get("name", "") for sheet in sheets)
        raise PipelineError(f"XLSX sheet not found: {sheet_name}. Available sheets: {available}.")

    relationship_id = selected_sheet.get(f"{{{namespace['rel']}}}id")
    relationships_root = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
    for relationship in relationships_root.findall("pkgrel:Relationship", namespace):
        if relationship.get("Id") == relationship_id:
            target = relationship.get("Target", "")
            return f"xl/{target.lstrip('/')}"

    raise PipelineError(f"XLSX sheet relationship not found: {relationship_id}")


def _parse_xlsx_value(cell: ET.Element, shared_strings: list[str], namespace: dict[str, str]) -> Any:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        inline = cell.find("main:is", namespace)
        return _xlsx_text(inline, namespace) if inline is not None else ""

    value_element = cell.find("main:v", namespace)
    if value_element is None or value_element.text is None:
        return ""

    raw_value = value_element.text
    if cell_type == "s":
        index = int(raw_value)
        return shared_strings[index] if index < len(shared_strings) else ""
    if cell_type == "b":
        return raw_value == "1"
    if cell_type == "str":
        return raw_value

    try:
        numeric_value = float(raw_value)
    except ValueError:
        return raw_value
    if numeric_value.is_integer():
        return int(numeric_value)
    return numeric_value


def read_xlsx(path: str, sheet: str | None = None) -> list[dict]:
    xlsx_path = Path(path)
    if not xlsx_path.exists():
        raise PipelineError(f"Input file not found: {xlsx_path}")

    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    try:
        with zipfile.ZipFile(xlsx_path) as workbook:
            shared_strings = _load_xlsx_shared_strings(workbook)
            sheet_path = _xlsx_sheet_path(workbook, sheet)
            sheet_root = ET.fromstring(workbook.read(sheet_path))
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        raise PipelineError(f"Invalid XLSX input file: {xlsx_path}. Reason: {exc}") from exc

    table: list[list[Any]] = []
    for row in sheet_root.findall(".//main:sheetData/main:row", namespace):
        values: list[Any] = []
        for cell in row.findall("main:c", namespace):
            reference = cell.get("r", "")
            column_index = _xlsx_column_index(reference)
            while len(values) <= column_index:
                values.append("")
            values[column_index] = _parse_xlsx_value(cell, shared_strings, namespace)
        table.append(values)

    if not table:
        raise PipelineError(f"Input file has no data rows: {xlsx_path}")

    headers = [str(header) for header in table[0]]
    rows = []
    for source_row in table[1:]:
        row = {}
        for index, header in enumerate(headers):
            if header:
                row[header] = source_row[index] if index < len(source_row) else ""
        rows.append(row)

    return _validate_rows(rows, xlsx_path)


def _sqlite_table_names(connection: sqlite3.Connection) -> list[str]:
    cursor = connection.execute(
        "select name from sqlite_master where type = 'table' and name not like 'sqlite_%' order by name"
    )
    return [row[0] for row in cursor.fetchall()]


def read_sqlite(path: str, table: str | None = None, query: str | None = None) -> list[dict]:
    sqlite_path = Path(path)
    if not sqlite_path.exists():
        raise PipelineError(f"Input file not found: {sqlite_path}")

    try:
        with sqlite3.connect(sqlite_path) as connection:
            connection.row_factory = sqlite3.Row
            if query:
                if not query.lstrip().lower().startswith(("select", "with")):
                    raise PipelineError("SQLite input query must be a read-only SELECT query.")
                cursor = connection.execute(query)
            else:
                table_names = _sqlite_table_names(connection)
                if table is None:
                    if len(table_names) != 1:
                        available = ", ".join(table_names) or "none"
                        raise PipelineError(
                            "SQLite input must specify 'table' when the database does not contain exactly one "
                            f"user table. Available tables: {available}."
                        )
                    table = table_names[0]
                if table not in table_names:
                    available = ", ".join(table_names) or "none"
                    raise PipelineError(f"SQLite table not found: {table}. Available tables: {available}.")
                escaped_table = table.replace('"', '""')
                cursor = connection.execute(f'select * from "{escaped_table}"')

            rows = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as exc:
        raise PipelineError(f"Invalid SQLite input file: {sqlite_path}. Reason: {exc}") from exc

    return _validate_rows(rows, sqlite_path)


def read_input_data(input_config: dict) -> list[dict]:
    input_type = input_config.get("type")
    input_path = input_config.get("path")

    if input_type == "csv":
        return read_csv(input_path)
    if input_type == "json":
        return read_json(input_path)
    if input_type == "xlsx":
        return read_xlsx(input_path, sheet=input_config.get("sheet"))
    if input_type == "sqlite":
        return read_sqlite(input_path, table=input_config.get("table"), query=input_config.get("query"))

    raise PipelineError(f"Unsupported input type: {input_type}")
