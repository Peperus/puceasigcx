"""Read/query helpers for reports domain."""

from django.db.models import Count, Q

from apps.academic_catalogs.models import Career
from apps.academic_catalogs.selectors import coordinator_career_ids
from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    user_has_role,
)
from apps.enrollment.models import (
    CourseEnrollmentStatus,
    CourseSection,
    CourseSectionStatus,
    Enrollment,
    TeachingAssignment,
    TeachingAssignmentStatus,
)
from apps.grading.models import GradeCalculationSnapshot
from apps.syllabus.models import Syllabus

MVP_REPORT_DEFINITIONS = {
    "students": {
        "title": "estudiantes-mvp",
        "headers": [
            "Periodo",
            "Carrera",
            "Codigo estudiante",
            "Estudiante",
            "Estado matricula",
            "Cursos matriculados",
        ],
    },
    "teachers": {
        "title": "docentes-asignados-mvp",
        "headers": [
            "Periodo",
            "Carrera",
            "Asignatura",
            "Paralelo",
            "Codigo docente",
            "Docente",
            "Rol",
            "Estado",
        ],
    },
    "courses": {
        "title": "cursos-activos-mvp",
        "headers": [
            "Periodo",
            "Carrera",
            "Asignatura",
            "Paralelo",
            "Modalidad",
            "Cupo",
            "Matriculados",
            "Estado",
        ],
    },
    "syllabi": {
        "title": "silabos-por-estado-mvp",
        "headers": [
            "Periodo",
            "Carrera",
            "Asignatura",
            "Paralelo",
            "Version",
            "Estado",
            "Docente titular",
        ],
    },
    "grades": {
        "title": "notas-por-curso-mvp",
        "headers": [
            "Periodo",
            "Carrera",
            "Asignatura",
            "Paralelo",
            "Modelo",
            "Estado libro",
            "Estudiante",
            "Nota final",
            "Estado final",
        ],
    },
}


def user_can_view_mvp_reports(user):
    return user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_CAREER_COORDINATOR,
        ROLE_ACADEMIC_DIRECTOR,
    )


def career_queryset_for_report_user(user):
    queryset = Career.objects.all()
    if user_has_role(user, ROLE_CAREER_COORDINATOR) and not user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_ACADEMIC_DIRECTOR,
    ):
        return queryset.filter(id__in=coordinator_career_ids(user))
    return queryset


def resolve_report_filters(query_params):
    filters = {}
    period = query_params.get("period")
    career = query_params.get("career")
    if period:
        filters["period"] = period
    if career:
        filters["career"] = career
    return filters


def apply_period_career_filters(queryset, filters, *, period_path, career_path):
    period = filters.get("period")
    if period:
        lookup = (
            f"{period_path}__id" if str(period).isdigit() else f"{period_path}__code"
        )
        queryset = queryset.filter(**{lookup: period})
    career = filters.get("career")
    if career:
        lookup = (
            f"{career_path}__id" if str(career).isdigit() else f"{career_path}__code"
        )
        queryset = queryset.filter(**{lookup: career})
    return queryset


def mvp_report_payload(*, report_type, user, filters):
    if report_type == "students":
        return _student_report(user=user, filters=filters)
    if report_type == "teachers":
        return _teacher_report(user=user, filters=filters)
    if report_type == "courses":
        return _course_report(user=user, filters=filters)
    if report_type == "syllabi":
        return _syllabus_report(user=user, filters=filters)
    if report_type == "grades":
        return _grade_report(user=user, filters=filters)
    raise KeyError(report_type)


def _student_report(*, user, filters):
    careers = career_queryset_for_report_user(user)
    queryset = Enrollment.objects.select_related(
        "period",
        "career",
        "student",
        "student__person",
    ).filter(career__in=careers)
    queryset = apply_period_career_filters(
        queryset,
        filters,
        period_path="period",
        career_path="career",
    ).annotate(
        enrolled_courses=Count(
            "course_enrollments",
            filter=Q(course_enrollments__status=CourseEnrollmentStatus.ENROLLED),
        )
    )
    rows = []
    data = []
    for enrollment in queryset.order_by(
        "career__name",
        "student__student_code",
    ):
        row = [
            enrollment.period.code,
            enrollment.career.name,
            enrollment.student.student_code,
            enrollment.student.person.full_name,
            enrollment.status,
            enrollment.enrolled_courses,
        ]
        rows.append(row)
        data.append(
            {
                "period": enrollment.period.code,
                "career": enrollment.career.name,
                "student_code": enrollment.student.student_code,
                "student_name": enrollment.student.person.full_name,
                "enrollment_status": enrollment.status,
                "enrolled_courses": enrollment.enrolled_courses,
            }
        )
    return data, rows


def _teacher_report(*, user, filters):
    careers = career_queryset_for_report_user(user)
    queryset = TeachingAssignment.objects.select_related(
        "course_section",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__subject",
        "teacher",
        "teacher__person",
    ).filter(
        course_section__offer__career__in=careers,
        status=TeachingAssignmentStatus.ACTIVE,
    )
    queryset = apply_period_career_filters(
        queryset,
        filters,
        period_path="course_section__offer__period",
        career_path="course_section__offer__career",
    )
    rows = []
    data = []
    for assignment in queryset.order_by(
        "course_section__offer__career__name",
        "course_section__subject__code",
        "teacher__teacher_code",
    ):
        course = assignment.course_section
        row = [
            course.offer.period.code,
            course.offer.career.name,
            f"{course.subject.code} - {course.subject.name}",
            course.parallel,
            assignment.teacher.teacher_code,
            assignment.teacher.person.full_name,
            assignment.role,
            assignment.status,
        ]
        rows.append(row)
        data.append(
            {
                "period": course.offer.period.code,
                "career": course.offer.career.name,
                "subject_code": course.subject.code,
                "subject_name": course.subject.name,
                "parallel": course.parallel,
                "teacher_code": assignment.teacher.teacher_code,
                "teacher_name": assignment.teacher.person.full_name,
                "role": assignment.role,
                "status": assignment.status,
            }
        )
    return data, rows


def _course_report(*, user, filters):
    careers = career_queryset_for_report_user(user)
    queryset = CourseSection.objects.select_related(
        "offer",
        "offer__period",
        "offer__career",
        "subject",
        "modality",
    ).filter(
        offer__career__in=careers,
        status=CourseSectionStatus.ACTIVE,
    )
    queryset = apply_period_career_filters(
        queryset,
        filters,
        period_path="offer__period",
        career_path="offer__career",
    )
    rows = []
    data = []
    for course in queryset.order_by("offer__career__name", "subject__code", "parallel"):
        row = [
            course.offer.period.code,
            course.offer.career.name,
            f"{course.subject.code} - {course.subject.name}",
            course.parallel,
            course.modality.name,
            course.capacity,
            course.enrolled_count,
            course.status,
        ]
        rows.append(row)
        data.append(
            {
                "period": course.offer.period.code,
                "career": course.offer.career.name,
                "subject_code": course.subject.code,
                "subject_name": course.subject.name,
                "parallel": course.parallel,
                "modality": course.modality.name,
                "capacity": course.capacity,
                "enrolled_count": course.enrolled_count,
                "status": course.status,
            }
        )
    return data, rows


def _syllabus_report(*, user, filters):
    careers = career_queryset_for_report_user(user)
    queryset = Syllabus.objects.select_related(
        "course_section",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__subject",
        "lead_teacher",
        "lead_teacher__person",
    ).filter(course_section__offer__career__in=careers)
    queryset = apply_period_career_filters(
        queryset,
        filters,
        period_path="course_section__offer__period",
        career_path="course_section__offer__career",
    )
    if filters.get("status"):
        queryset = queryset.filter(status=filters["status"])
    rows = []
    data = []
    for syllabus in queryset.order_by(
        "status",
        "course_section__offer__career__name",
        "course_section__subject__code",
    ):
        course = syllabus.course_section
        row = [
            course.offer.period.code,
            course.offer.career.name,
            f"{course.subject.code} - {course.subject.name}",
            course.parallel,
            syllabus.version,
            syllabus.status,
            syllabus.lead_teacher.person.full_name,
        ]
        rows.append(row)
        data.append(
            {
                "period": course.offer.period.code,
                "career": course.offer.career.name,
                "subject_code": course.subject.code,
                "subject_name": course.subject.name,
                "parallel": course.parallel,
                "version": syllabus.version,
                "status": syllabus.status,
                "lead_teacher": syllabus.lead_teacher.person.full_name,
            }
        )
    return data, rows


def _grade_report(*, user, filters):
    careers = career_queryset_for_report_user(user)
    queryset = GradeCalculationSnapshot.objects.filter(
        is_current=True,
        gradebook__course_section__offer__career__in=careers,
    ).select_related(
        "gradebook",
        "gradebook__course_section",
        "gradebook__course_section__offer",
        "gradebook__course_section__offer__period",
        "gradebook__course_section__offer__career",
        "gradebook__course_section__subject",
        "course_enrollment",
        "course_enrollment__enrollment",
        "course_enrollment__enrollment__student",
        "course_enrollment__enrollment__student__person",
    )
    queryset = apply_period_career_filters(
        queryset,
        filters,
        period_path="gradebook__course_section__offer__period",
        career_path="gradebook__course_section__offer__career",
    )
    if filters.get("grading_model"):
        queryset = queryset.filter(grading_model=filters["grading_model"])
    if filters.get("status"):
        queryset = queryset.filter(final_status=filters["status"])
    rows = []
    data = []
    for snapshot in queryset.order_by(
        "gradebook__course_section__offer__career__name",
        "gradebook__course_section__subject__code",
        "course_enrollment__enrollment__student__student_code",
    ):
        course = snapshot.gradebook.course_section
        student = snapshot.course_enrollment.enrollment.student
        row = [
            course.offer.period.code,
            course.offer.career.name,
            f"{course.subject.code} - {course.subject.name}",
            course.parallel,
            snapshot.grading_model,
            snapshot.gradebook.status,
            student.person.full_name,
            str(snapshot.final_score),
            snapshot.final_status,
        ]
        rows.append(row)
        data.append(
            {
                "period": course.offer.period.code,
                "career": course.offer.career.name,
                "subject_code": course.subject.code,
                "subject_name": course.subject.name,
                "parallel": course.parallel,
                "grading_model": snapshot.grading_model,
                "gradebook_status": snapshot.gradebook.status,
                "student_name": student.person.full_name,
                "student_code": student.student_code,
                "final_score": str(snapshot.final_score),
                "final_status": snapshot.final_status,
            }
        )
    return data, rows
