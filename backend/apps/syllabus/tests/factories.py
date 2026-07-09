from decimal import Decimal

from apps.enrollment.models import TeachingAssignment, TeachingRole
from apps.enrollment.tests.factories import make_course_section
from apps.people.tests.factories import make_person, make_teacher
from apps.syllabus.models import (
    AchievementLevelCode,
    BibliographyType,
    CompetencyType,
    LearningOutcomeType,
    Syllabus,
    SyllabusAchievementLevel,
    SyllabusBibliography,
    SyllabusCompetency,
    SyllabusCriterion,
    SyllabusLearningOutcome,
    SyllabusWeeklyPlan,
)


def make_assigned_teacher(course_section=None, user=None, code="SIL"):
    if course_section is None:
        course_section = make_course_section(code)
    person = make_person(
        identification_number=f"PER-DOC-{code}",
        first_name="Docente",
        last_name=f"Sintetico {code}",
        user=user,
    )
    teacher = make_teacher(person=person, teacher_code=f"DOC-{code}")
    TeachingAssignment.objects.create(
        course_section=course_section,
        teacher=teacher,
        role=TeachingRole.LEAD,
    )
    return teacher


def make_syllabus(code="SIL", user=None, **overrides):
    course_section = overrides.pop("course_section", make_course_section(code))
    lead_teacher = overrides.pop(
        "lead_teacher",
        make_assigned_teacher(course_section=course_section, user=user, code=code),
    )
    data = {
        "course_section": course_section,
        "lead_teacher": lead_teacher,
        "subject_description": "Descripcion sintetica de la asignatura.",
        "methodology": "Metodologia activa con recursos sinteticos.",
    }
    data.update(overrides)
    return Syllabus.objects.create(**data)


def add_required_learning_outcomes(syllabus):
    outcomes = []
    for outcome_type in (LearningOutcomeType.CAREER, LearningOutcomeType.SUBJECT):
        for order in range(1, 4):
            outcomes.append(
                SyllabusLearningOutcome.objects.create(
                    syllabus=syllabus,
                    outcome_type=outcome_type,
                    code=f"{outcome_type.value.upper()}-{order}",
                    text=f"Resultado sintetico {outcome_type.value} {order}",
                    order=order,
                )
            )
    return outcomes


def add_complete_rubrics(syllabus):
    subject_outcomes = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    )
    for outcome in subject_outcomes:
        for order in range(1, 5):
            criterion = SyllabusCriterion.objects.create(
                syllabus=syllabus,
                learning_outcome=outcome,
                name=f"Criterio {outcome.order}.{order}",
                description="Criterio sintetico.",
                weight=Decimal("25.00"),
                order=order,
            )
            for level in AchievementLevelCode:
                SyllabusAchievementLevel.objects.create(
                    criterion=criterion,
                    level=level,
                    description=f"Descriptor sintetico {level.value}.",
                )


def add_minimum_competency(syllabus):
    return SyllabusCompetency.objects.create(
        syllabus=syllabus,
        competency_type=CompetencyType.TRANSVERSAL,
        text="Competencia sintetica transversal.",
        order=1,
    )


def add_minimum_bibliography(syllabus):
    return SyllabusBibliography.objects.create(
        syllabus=syllabus,
        bibliography_type=BibliographyType.BASIC,
        apa_reference="Autoria sintetica. (2026). Recurso academico sintetico.",
        library_code="BIB-SINT",
        copies=1,
        order=1,
    )


def add_minimum_weekly_plan(syllabus):
    outcome = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    ).first()
    return SyllabusWeeklyPlan.objects.create(
        syllabus=syllabus,
        learning_outcome=outcome,
        week_number=1,
        week_label="Semana 1",
        knowledge_dimension="Conceptual",
        contact_strategy="Clase dialogada sintetica.",
        contact_hours=Decimal("2.00"),
        practical_strategy="Taller sintetico.",
        practical_hours=Decimal("1.00"),
        autonomous_strategy="Lectura sintetica.",
        autonomous_hours=Decimal("2.00"),
    )


def make_complete_syllabus(code="SIL", user=None):
    syllabus = make_syllabus(code=code, user=user)
    add_minimum_competency(syllabus)
    add_required_learning_outcomes(syllabus)
    add_complete_rubrics(syllabus)
    add_minimum_bibliography(syllabus)
    add_minimum_weekly_plan(syllabus)
    return syllabus
