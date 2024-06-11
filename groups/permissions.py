from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Group, Product, Store

class IsGroupAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            group_pk = view.kwargs.get('pk') or view.kwargs.get('group_pk')
            group = get_object_or_404(Group, pk=group_pk)

            return request.user == group.admin
        return False
        
class IsGroupMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            group_pk = view.kwargs.get('group_pk') or view.kwargs.get('pk')

            return request.user.group_id == group_pk
        return False
    
class IsGroupless(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            group_id = request.user.group_id
            return not group_id
        return False
