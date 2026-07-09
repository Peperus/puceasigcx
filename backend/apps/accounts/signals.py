from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.audit.services import log_event

from .services import ensure_user_profile, set_primary_role_from_groups


@receiver(post_save, sender=get_user_model())
def create_profile_and_audit_user(sender, instance, created, **kwargs):
    ensure_user_profile(instance)
    if created:
        log_event(
            action="user_created",
            module="accounts",
            user=instance,
            model_name="User",
            object_id=str(instance.pk),
            new_data={"email": instance.email},
        )


@receiver(m2m_changed, sender=get_user_model().groups.through)
def audit_role_changes(sender, instance, action, pk_set, **kwargs):
    if action not in {"post_add", "post_remove", "post_clear"}:
        return

    set_primary_role_from_groups(instance)
    log_event(
        action="role_changed",
        module="accounts",
        user=instance,
        model_name="User",
        object_id=str(instance.pk),
        new_data={
            "action": action,
            "group_ids": sorted(pk_set) if pk_set else [],
        },
    )
