from rest_framework import permissions


class OwnerOrAdminOrModerator(permissions.BasePermission):
