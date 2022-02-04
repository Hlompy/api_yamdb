from rest_framework import permissions


class OwnerOrAdminOrModerator(permissions.BasePermission):
    pass

class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                )

class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.is_admin)
