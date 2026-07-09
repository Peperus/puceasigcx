"""Transactional services for accounts domain."""

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import UserProfile
from .roles import ROLE_NAME_BY_CODE


@transaction.atomic
def ensure_user_profile(user):
    profile, _created = UserProfile.objects.get_or_create(user=user)
    return profile


@transaction.atomic
def update_current_user(user, *, names=None, last_names=None, phone=None):
    if names is not None:
        user.names = names
    if last_names is not None:
        user.last_names = last_names
    if phone is not None:
        user.phone = phone

    user.save(update_fields=["names", "last_names", "phone", "updated_at"])
    ensure_user_profile(user)
    return user


def get_user_by_email(email):
    if not email:
        return None

    return get_user_model().objects.filter(email__iexact=email).first()


@transaction.atomic
def set_primary_role_from_groups(user):
    profile = ensure_user_profile(user)
    first_group = user.groups.order_by("name").first()
    profile.primary_role = first_group.name if first_group else ""
    profile.save(update_fields=["primary_role", "updated_at"])
    return profile


def role_name_from_code(role_code):
    return ROLE_NAME_BY_CODE.get(role_code, role_code)
