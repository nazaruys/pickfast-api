from rest_framework import permissions

class IsUsersProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            pk = view.kwargs.get('pk')
            return str(request.user.pk) == pk
        return False