"""Serializers for accounts API resources."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.audit.services import log_event

from .roles import get_user_role_codes
from .selectors import get_user_session_payload
from .services import ensure_user_profile, get_user_by_email


class InstitutionalTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["roles"] = get_user_role_codes(user)
        return token

    def validate(self, attrs):
        email = attrs.get("email", "")
        try:
            data = super().validate(attrs)
        except Exception:
            user = get_user_by_email(email)
            log_event(
                action="login_failed",
                module="authentication",
                user=user if user and user.is_active else None,
                model_name="User",
                object_id=str(user.pk) if user else "",
                new_data={"email": email.lower()},
                request=self.context.get("request"),
            )
            raise

        data["user"] = get_user_session_payload(self.user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = RefreshToken(attrs["refresh"])
        return attrs

    def save(self, **kwargs):
        self.token.blacklist()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        email = self.validated_data["email"]
        user = get_user_by_email(email)

        if user and user.is_active:
            uid = urlsafe_base64_encode(str(user.pk).encode())
            token = default_token_generator.make_token(user)
            send_mail(
                subject="Recuperacion de contrasena PUCEASIG",
                message=(
                    "Se solicito recuperar la contrasena de PUCEASIG.\n"
                    f"UID: {uid}\n"
                    f"Token: {token}\n"
                    "Si no solicitaste este cambio, ignora este mensaje."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    default_error_messages = {
        "invalid_token": _("El token de recuperacion no es valido o expiro.")
    }

    def validate(self, attrs):
        user = self._get_user(attrs["uid"])
        if user is None or not default_token_generator.check_token(
            user, attrs["token"]
        ):
            self.fail("invalid_token")

        validate_password(attrs["new_password"], user)
        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password", "updated_at"])
        log_event(
            action="password_changed",
            module="authentication",
            user=user,
            model_name="User",
            object_id=str(user.pk),
            request=self.context.get("request"),
        )
        return user

    def _get_user(self, uid):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            return get_user_model().objects.get(pk=user_id, is_active=True)
        except TypeError, ValueError, OverflowError, get_user_model().DoesNotExist:
            return None


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    names = serializers.CharField(max_length=150, required=False)
    last_names = serializers.CharField(max_length=150, required=False)
    full_name = serializers.CharField(read_only=True)
    phone = serializers.CharField(max_length=30, allow_blank=True, required=False)
    is_active = serializers.BooleanField(read_only=True)
    roles = serializers.ListField(child=serializers.CharField(), read_only=True)
    profile = serializers.DictField(read_only=True)

    writable_fields = {"names", "last_names", "phone"}

    def to_representation(self, instance):
        ensure_user_profile(instance)
        return get_user_session_payload(instance)

    def to_internal_value(self, data):
        filtered_data = {
            key: value for key, value in data.items() if key in self.writable_fields
        }
        return super().to_internal_value(filtered_data)
