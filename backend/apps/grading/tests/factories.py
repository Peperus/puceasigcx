from apps.academic_catalogs.models import GradingSystem
from apps.enrollment.models import CourseEnrollment
from apps.enrollment.tests.factories import make_course_section, make_enrollment
from apps.grading.models import Gradebook, GradeItem, GradeItemType
from apps.syllabus.models import Syllabus, SyllabusStatus
from apps.syllabus.tests.factories import (
    add_complete_rubrics,
    add_minimum_bibliography,
    add_minimum_competency,
    add_minimum_weekly_plan,
    add_required_learning_outcomes,
    make_assigned_teacher,
)


def make_ready_course(code="GRADE", grading_model="S1"):
    course_section = make_course_section(code=code)
    grading_system, _ = GradingSystem.objects.get_or_create(
        code=grading_model,
        defaults={"name": f"Sistema {grading_model}", "is_active": True},
    )
    course_section.grading_system = grading_system
    course_section.save()
    return course_section


def make_approved_syllabus(code="GRADE", grading_model="S1"):
    course_section = make_ready_course(code=code, grading_model=grading_model)
    syllabus = make_grading_syllabus(code=code, course_section=course_section)
    add_minimum_competency(syllabus)
    add_required_learning_outcomes(syllabus)
    add_complete_rubrics(syllabus)
    add_minimum_bibliography(syllabus)
    add_minimum_weekly_plan(syllabus)
    syllabus.status = SyllabusStatus.APPROVED
    syllabus.save()
    return syllabus


def make_grading_syllabus(code="GRADE", course_section=None):
    if course_section is None:
        course_section = make_ready_course(code=code)
    lead_teacher = make_assigned_teacher(course_section=course_section, code=code)
    return Syllabus.objects.create(
        course_section=course_section,
        lead_teacher=lead_teacher,
        subject_description="Descripcion sintetica de la asignatura.",
        methodology="Metodologia activa con recursos sinteticos.",
    )


def make_gradebook(code="GRADE", grading_model="S1"):
    syllabus = make_approved_syllabus(code=code, grading_model=grading_model)
    return Gradebook.objects.create(
        course_section=syllabus.course_section,
        syllabus=syllabus,
    )


def make_course_enrollment(code="GRADE", course_section=None):
    if course_section is None:
        course_section = make_ready_course(code=code)
    enrollment = make_enrollment(code=code, course_section=course_section)
    return CourseEnrollment.objects.create(
        enrollment=enrollment,
        course_section=course_section,
    )


def add_s1_s2_structure(gradebook):
    items = []
    for outcome_order in range(1, 4):
        outcome = GradeItem.objects.create(
            gradebook=gradebook,
            item_type=GradeItemType.LEARNING_OUTCOME,
            name=f"RA {outcome_order}",
            order=outcome_order,
        )
        criterion = GradeItem.objects.create(
            gradebook=gradebook,
            parent=outcome,
            item_type=GradeItemType.CRITERION,
            name=f"Criterio {outcome_order}",
            order=1,
            weight=100,
        )
        activity = GradeItem.objects.create(
            gradebook=gradebook,
            parent=criterion,
            item_type=GradeItemType.ACTIVITY,
            name=f"Actividad {outcome_order}",
            order=1,
            weight=100,
        )
        recovery = GradeItem.objects.create(
            gradebook=gradebook,
            parent=outcome,
            item_type=GradeItemType.RECOVERY,
            name=f"Recuperacion {outcome_order}",
            order=2,
        )
        items.append(
            {
                "outcome": outcome,
                "criterion": criterion,
                "activity": activity,
                "recovery": recovery,
            }
        )
    return items
