"""Transactional services for reports domain."""

import csv
import zipfile
from datetime import UTC, datetime
from io import BytesIO
from xml.sax.saxutils import escape

from django.http import HttpResponse

from apps.audit.services import log_event

GRADE_EXPORT_HEADERS = [
    "Periodo",
    "Carrera",
    "Asignatura",
    "Paralelo",
    "Modelo",
    "Estudiante",
    "Codigo estudiante",
    "Nota final",
    "Letra",
    "Estado",
    "Fecha calculo",
]


def grade_snapshot_export_rows(snapshots):
    rows = []
    for snapshot in snapshots:
        gradebook = snapshot.gradebook
        course = gradebook.course_section
        student = snapshot.course_enrollment.enrollment.student
        rows.append(
            [
                course.offer.period.code,
                course.offer.career.name,
                f"{course.subject.code} - {course.subject.name}",
                course.parallel,
                snapshot.grading_model,
                student.person.full_name,
                student.student_code,
                str(snapshot.final_score),
                snapshot.final_letter,
                snapshot.final_status,
                snapshot.calculated_at.isoformat(),
            ]
        )
    return rows


def grade_export_response(*, snapshots, export_format, user, filters, request=None):
    rows = grade_snapshot_export_rows(snapshots)
    generated_at = datetime.now(UTC).isoformat()
    filename = f"acta-calificaciones-{generated_at[:10]}"

    log_event(
        action="grade_report_exported",
        module="reports",
        user=user,
        model_name="GradeCalculationSnapshot",
        new_data={"filters": filters, "format": export_format, "rows": len(rows)},
        request=request,
    )

    if export_format == "xlsx":
        response = HttpResponse(
            _xlsx_bytes(rows, generated_at),
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
        return response

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Generado", generated_at])
    writer.writerow([])
    writer.writerow(GRADE_EXPORT_HEADERS)
    writer.writerows(rows)
    return response


def _xlsx_bytes(rows, generated_at):
    workbook = BytesIO()
    sheet_rows = [["Generado", generated_at], [], GRADE_EXPORT_HEADERS, *rows]
    with zipfile.ZipFile(workbook, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _content_types_xml())
        archive.writestr("_rels/.rels", _root_rels_xml())
        archive.writestr("xl/workbook.xml", _workbook_xml())
        archive.writestr("xl/_rels/workbook.xml.rels", _workbook_rels_xml())
        archive.writestr("xl/worksheets/sheet1.xml", _worksheet_xml(sheet_rows))
    return workbook.getvalue()


def _content_types_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-'
        'package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.'
        'openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )


def _root_rels_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
        'relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )


def _workbook_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships">'
        '<sheets><sheet name="Acta" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )


def _workbook_rels_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
        'relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )


def _worksheet_xml(rows):
    xml_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for column_index, value in enumerate(row, start=1):
            reference = f"{_column_letter(column_index)}{row_index}"
            cells.append(
                f'<c r="{reference}" t="inlineStr"><is><t>'
                f"{escape(str(value))}</t></is></c>"
            )
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        "</worksheet>"
    )


def _column_letter(index):
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters
