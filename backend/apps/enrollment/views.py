from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from .models import (
    AcademicOffer,
    CourseEnrollment,
    CourseSection,
    Enrollment,
    Homologation,
    TeachingAssignment,
)
from .selectors import (
    user_can_manage_enrollment_records,
    user_can_manage_object_for_career,
    user_can_manage_offer_records,
    user_can_view_enrollment_records,
    visible_academic_offers_for_user,
    visible_course_enrollments_for_user,
    visible_course_sections_for_user,
    visible_enrollments_for_user,
    visible_homologations_for_user,
    visible_teaching_assignments_for_user,
)
from .serializers import (
    AcademicOfferSerializer,
    CourseEnrollmentSerializer,
    CourseSectionSerializer,
    EnrollmentSerializer,
    HomologationSerializer,
    TeachingAssignmentSerializer,
)


class CanReadOrManageEnrollment(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_enrollment_records(request.user)
        if getattr(view, "enrollment_write_only_staff", False):
            return user_can_manage_enrollment_records(request.user)
        return user_can_manage_offer_records(request.user)


class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [CanReadOrManageEnrollment]
    filter_backends = [SearchFilter, OrderingFilter]

    def _ensure_can_manage_career(self, career_id):
        if not user_can_manage_object_for_career(self.request.user, career_id):
            raise PermissionDenied("No tiene permisos para gestionar esta carrera.")

    def _career_id_from_validated_data(self, validated_data):
        if "career" in validated_data:
            return validated_data["career"].id
        if "offer" in validated_data:
            return validated_data["offer"].career_id
        if "course_section" in validated_data:
            return validated_data["course_section"].offer.career_id
        if "enrollment" in validated_data:
            return validated_data["enrollment"].career_id
        if "student" in validated_data:
            return validated_data["student"].career_id
        return None

    def perform_create(self, serializer):
        career_id = self._career_id_from_validated_data(serializer.validated_data)
        if career_id is not None:
            self._ensure_can_manage_career(career_id)
        serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        career_id = self._career_id_from_instance(instance)
        self._ensure_can_manage_career(career_id)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_can_manage_career(self._career_id_from_instance(instance))
        instance.delete()

    def _career_id_from_instance(self, instance):
        if isinstance(instance, AcademicOffer):
            return instance.career_id
        if isinstance(instance, CourseSection):
            return instance.offer.career_id
        if isinstance(instance, TeachingAssignment):
            return instance.course_section.offer.career_id
        if isinstance(instance, Enrollment):
            return instance.career_id
        if isinstance(instance, CourseEnrollment):
            return instance.course_section.offer.career_id
        if isinstance(instance, Homologation):
            return instance.student.career_id
        raise PermissionDenied("Recurso no soportado.")


class AcademicOfferViewSet(EnrollmentViewSet):
    serializer_class = AcademicOfferSerializer
    search_fields = (
        "period__code",
        "career__code",
        "career__name",
        "study_plan__code",
        "level__name",
    )
    ordering_fields = ("period__start_date", "career__name", "level__order", "status")

    def get_queryset(self):
        return visible_academic_offers_for_user(self.request.user)


class CourseSectionViewSet(EnrollmentViewSet):
    serializer_class = CourseSectionSerializer
    search_fields = (
        "offer__period__code",
        "offer__career__name",
        "subject__code",
        "subject__name",
        "parallel",
        "classroom",
    )
    ordering_fields = ("subject__code", "parallel", "capacity", "status")

    def get_queryset(self):
        return visible_course_sections_for_user(self.request.user)


class TeachingAssignmentViewSet(EnrollmentViewSet):
    serializer_class = TeachingAssignmentSerializer
    search_fields = (
        "course_section__subject__code",
        "course_section__subject__name",
        "teacher__teacher_code",
        "teacher__person__first_name",
        "teacher__person__last_name",
    )
    ordering_fields = ("role", "status", "teacher__teacher_code")

    def get_queryset(self):
        return visible_teaching_assignments_for_user(self.request.user)


class EnrollmentRecordViewSet(EnrollmentViewSet):
    serializer_class = EnrollmentSerializer
    enrollment_write_only_staff = True
    search_fields = (
        "student__student_code",
        "student__person__first_name",
        "student__person__last_name",
        "period__code",
        "career__name",
    )
    ordering_fields = ("period__start_date", "student__student_code", "status")

    def get_queryset(self):
        return visible_enrollments_for_user(self.request.user)


class CourseEnrollmentViewSet(EnrollmentViewSet):
    serializer_class = CourseEnrollmentSerializer
    enrollment_write_only_staff = True
    search_fields = (
        "enrollment__student__student_code",
        "enrollment__student__person__first_name",
        "enrollment__student__person__last_name",
        "course_section__subject__code",
        "course_section__subject__name",
    )
    ordering_fields = ("enrolled_at", "status", "course_section__subject__code")

    def get_queryset(self):
        return visible_course_enrollments_for_user(self.request.user)


class HomologationViewSet(EnrollmentViewSet):
    serializer_class = HomologationSerializer
    enrollment_write_only_staff = True
    search_fields = (
        "student__student_code",
        "student__person__first_name",
        "student__person__last_name",
        "subject__code",
        "subject__name",
        "resolution_reference",
    )
    ordering_fields = ("created_at", "status", "subject__code")

    def get_queryset(self):
        return visible_homologations_for_user(self.request.user)
