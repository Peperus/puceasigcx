from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_STUDENT, ROLE_TEACHER, user_has_role
from apps.audit.services import log_event

from .selectors import (
    person_for_user,
    user_can_manage_people,
    user_can_view_people_staff,
    visible_people_for_user,
)
from .serializers import PersonSerializer


def _person_snapshot(person):
    return {
        "id": person.pk,
        "user_id": person.user_id,
        "identification_number": person.identification_number,
        "institutional_email": person.institutional_email,
        "is_active": person.is_active,
    }


class CanReadOrManagePeople(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_people_staff(request.user) or bool(
                person_for_user(request.user)
                and user_has_role(request.user, ROLE_TEACHER, ROLE_STUDENT)
            )
        return user_can_manage_people(request.user)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = [CanReadOrManagePeople]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (
        "identification_number",
        "first_name",
        "last_name",
        "institutional_email",
        "personal_email",
    )
    ordering_fields = ("last_name", "first_name", "identification_number")

    def get_queryset(self):
        return visible_people_for_user(self.request.user)

    def perform_create(self, serializer):
        person = serializer.save()
        log_event(
            action="person_created",
            module="people",
            user=self.request.user,
            model_name="Person",
            object_id=person.pk,
            new_data=_person_snapshot(person),
            request=self.request,
        )

    def perform_update(self, serializer):
        previous = _person_snapshot(serializer.instance)
        person = serializer.save()
        log_event(
            action="person_updated",
            module="people",
            user=self.request.user,
            model_name="Person",
            object_id=person.pk,
            previous_data=previous,
            new_data=_person_snapshot(person),
            request=self.request,
        )

    def perform_destroy(self, instance):
        previous = _person_snapshot(instance)
        object_id = instance.pk
        instance.delete()
        log_event(
            action="person_deleted",
            module="people",
            user=self.request.user,
            model_name="Person",
            object_id=object_id,
            previous_data=previous,
            request=self.request,
        )
