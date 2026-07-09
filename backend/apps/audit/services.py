"""Transactional services for audit domain."""

from .models import AuditLog


def log_event(
    *,
    action,
    module,
    user=None,
    model_name="",
    object_id="",
    previous_data=None,
    new_data=None,
    reason="",
    request=None,
):
    ip_address = None
    user_agent = ""

    if request is not None:
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip_address = (
            forwarded_for.split(",")[0].strip()
            if forwarded_for
            else request.META.get("REMOTE_ADDR")
        )
        user_agent = request.META.get("HTTP_USER_AGENT", "")

    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", True) else None,
        action=action,
        module=module,
        model_name=model_name,
        object_id=str(object_id) if object_id else "",
        previous_data=previous_data or {},
        new_data=new_data or {},
        reason=reason,
        ip_address=ip_address or None,
        user_agent=user_agent,
    )
