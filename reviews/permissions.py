from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the review
        return obj.user == request.user
    
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Allow only owners of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for anyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Allow write requests only for the owner
        return obj.user == request.user




from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for anyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions only for the owner of the review
        return obj.user == request.user


