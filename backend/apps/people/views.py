from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_STUDENT, ROLE_TEACHER, user_has_role

from .selectors import (
    person_for_user,
    user_can_manage_people,
    user_can_view_people_staff,
    visible_people_for_user,
)
from .serializers import PersonSerializer


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
