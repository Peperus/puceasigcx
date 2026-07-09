"""Read/query helpers for accounts domain."""

from .roles import get_user_role_codes


def get_user_session_payload(user):
    profile = getattr(user, "profile", None)
    return {
        "id": user.id,
        "email": user.email,
        "names": user.names,
        "last_names": user.last_names,
        "full_name": user.full_name,
        "phone": user.phone,
        "is_active": user.is_active,
        "roles": get_user_role_codes(user),
        "profile": {
            "primary_role": profile.primary_role if profile else "",
            "must_change_password": (
                profile.must_change_password if profile else False
            ),
            "security_questions_configured": (
                profile.security_questions_configured if profile else False
            ),
        },
    }
