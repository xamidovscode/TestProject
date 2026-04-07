from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVerifiedUser(BasePermission):
    message = "Email tasdiqlanmagan. Avval verifying qiling."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.is_verified

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_verified and obj.author == request.user
