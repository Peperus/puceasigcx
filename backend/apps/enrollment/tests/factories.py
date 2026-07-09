from apps.academic_catalogs.tests.factories import (
    make_career,
    make_level,
    make_modality,
    make_period,
    make_plan,
    make_subject,
)
from apps.enrollment.models import (
    AcademicOffer,
    CourseSection,
    CourseSectionStatus,
    Enrollment,
)
from apps.people.tests.factories import make_student, make_teacher


def make_offer(code="OFFER", coordinator_user=None):
    period = make_period(code=f"PER-{code}")
    career = make_career(code=f"CAR-{code}", coordinator_user=coordinator_user)
    plan = make_plan(code=f"PLAN-{code}", career=career)
    if coordinator_user is not None:
        plan.career.coordinator_user = coordinator_user
        plan.career.save()
    level = make_level(study_plan=plan, number=1)
    return AcademicOffer.objects.create(
        period=period,
        career=plan.career,
        study_plan=plan,
        level=level,
    )


def make_course_section(
    code="COURSE",
    offer=None,
    capacity=2,
    status=CourseSectionStatus.ACTIVE,
):
    if offer is None:
        offer = make_offer(code)
    subject = make_subject(career=offer.career, code=f"SUB-{code}")
    modality = make_modality(code=f"MOD-{code}")
    grading_system = subject.default_grading_system
    return CourseSection.objects.create(
        offer=offer,
        subject=subject,
        parallel="A",
        capacity=capacity,
        modality=modality,
        grading_system=grading_system,
        status=status,
    )


def make_enrollment(code="ENR", course_section=None, student=None):
    if course_section is None:
        course_section = make_course_section(code)
    if student is None:
        student = make_student(
            career=course_section.offer.career,
            student_code=f"EST-{code}",
        )
    return Enrollment.objects.create(
        student=student,
        period=course_section.offer.period,
        career=student.career,
        study_plan=student.study_plan,
    )


def make_active_teacher(code="TEA"):
    return make_teacher(teacher_code=f"DOC-{code}")
