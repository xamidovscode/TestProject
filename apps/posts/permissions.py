from rest_framework.permissions import BasePermission


class IsVerifiedUser(BasePermission):
    message = "Email tasdiqlanmagan. Avval verifying qiling."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.is_verified