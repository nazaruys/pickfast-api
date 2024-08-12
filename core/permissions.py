from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import User

class IsUsersProfileOrGroupAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_pk = view.kwargs.get('pk')
            # If user updates own profile
            if str(request.user.pk) == user_pk:
                return True 
            user = get_object_or_404(User, pk=user_pk)
            updated_fields = request.data.keys()
            # If admin of group of the user updates group_id of user
            if user.group and request.user == user.group.admin and (len(updated_fields) == 1 and 'group_id' in updated_fields):
                return True
            return False
        return False
    