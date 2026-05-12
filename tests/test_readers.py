import sqlite3
import zipfile

from analysis_framework.dataio import read_input_data, read_sqlite, read_xlsx


def _xlsx_column_name(index):
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _xlsx_cell(value, row_index, column_index):
    reference = f"{_xlsx_column_name(column_index)}{row_index}"
    if value == "":
        return f'<c r="{reference}"/>'
    if isinstance(value, (int, float)):
        return f'<c r="{reference}"><v>{value}</v></c>'
    return f'<c r="{reference}" t="inlineStr"><is><t>{value}</t></is></c>'


def _write_xlsx(path, rows, sheet_name="people_metrics"):
    sheet_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = [_xlsx_cell(value, row_index, column_index) for column_index, value in enumerate(row, start=1)]
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    with zipfile.ZipFile(path, "w") as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>""",
        )
        workbook.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""",
        )
        workbook.writestr(
            "xl/workbook.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="{sheet_name}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>""",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""",
        )
        workbook.writestr(
            "xl/worksheets/sheet1.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    {"".join(sheet_rows)}
  </sheetData>
</worksheet>""",
        )


def test_read_xlsx_converts_sheet_to_rows(tmp_path):
    path = tmp_path / "people_metrics.xlsx"
    _write_xlsx(
        path,
        [
            ["id", "age", "income", "score", "city"],
            [1, 25, 5000, 80, "Shanghai"],
            [2, "", 6200, 88, "Beijing"],
        ],
    )

    rows = read_xlsx(str(path), sheet="people_metrics")

    assert rows == [
        {"id": 1, "age": 25, "income": 5000, "score": 80, "city": "Shanghai"},
        {"id": 2, "age": "", "income": 6200, "score": 88, "city": "Beijing"},
    ]


def test_read_sqlite_converts_table_to_rows(tmp_path):
    path = tmp_path / "people_metrics.sqlite"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "create table people_metrics (id integer, age integer, income integer, score integer, city text)"
        )
        connection.executemany(
            "insert into people_metrics values (?, ?, ?, ?, ?)",
            [
                (1, 25, 5000, 80, "Shanghai"),
                (2, None, 6200, 88, "Beijing"),
            ],
        )

    rows = read_sqlite(str(path), table="people_metrics")

    assert rows == [
        {"id": 1, "age": 25, "income": 5000, "score": 80, "city": "Shanghai"},
        {"id": 2, "age": None, "income": 6200, "score": 88, "city": "Beijing"},
    ]


def test_read_input_data_dispatches_xlsx_and_sqlite(tmp_path):
    xlsx_path = tmp_path / "people_metrics.xlsx"
    _write_xlsx(xlsx_path, [["id", "city"], [1, "Shanghai"]])

    sqlite_path = tmp_path / "people_metrics.sqlite"
    with sqlite3.connect(sqlite_path) as connection:
        connection.execute("create table people_metrics (id integer, city text)")
        connection.execute("insert into people_metrics values (?, ?)", (1, "Shanghai"))

    assert read_input_data({"type": "xlsx", "path": str(xlsx_path)}) == [{"id": 1, "city": "Shanghai"}]
    assert read_input_data({"type": "sqlite", "path": str(sqlite_path), "table": "people_metrics"}) == [
        {"id": 1, "city": "Shanghai"}
    ]
