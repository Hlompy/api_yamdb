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


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.is_moderator)


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (request.user.is_staff or request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user
                    or request.method == 'POST'
                    and request.user.is_authenticated):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
