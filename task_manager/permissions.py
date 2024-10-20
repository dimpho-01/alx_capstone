from rest_framework import permissions

# # Ensures a user can only update or delete their own account details and no one else's.
# class IsSelfOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if not request.user.is_authenticated:
#             return False
        
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return obj == request.user
    
class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow admin users to view any user 
    or the user to view their own information.
    """

    def has_object_permission(self, request, view, obj):
        # Allow user to see their own information
        if request.user == obj:
            return True
            
        # Allow admin users to view any information
        if request.user.is_staff:
            return True
            
        # Deny access if neither of the above is true
        return False