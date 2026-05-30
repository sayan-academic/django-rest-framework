from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):
    message = "You cannot edit or delete a product you did not create."

    def has_permission(self, request, view):
        # This mathematically blocks anyone who isn't a valid, logged-in user in the DB.
        # If they don't exist, request.user.is_authenticated evaluates to False.
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # 1. If it's a GET, HEAD, or OPTIONS request, let the authenticated user view it.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 2. If it's a PUT, PATCH, or DELETE request, verify ownership.
        # obj.owner is the ForeignKey from your Product model.
        return obj.owner == request.user