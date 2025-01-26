from rest_framework import permissions

class IsStaffPermission(permissions.DjangoModelPermissions):
    message="Only Admin are Allowed!"
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        print(request.user)
        print(request.user.is_staff)
        user=request.user
        if user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            if request.method != "GET":
                return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user=request.user
        if user.is_staff:
            return True
        return False
