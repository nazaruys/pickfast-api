from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Group, Store, Product
from .serializers import GroupSerializer, StoreSerializer, ProductSerializer, MembersUserSerializer
from .permissions import IsGroupAdmin, IsGroupMember, IsGroupless

User = get_user_model()

class GroupViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            self.permission_classes = [AllowAny]
        else:
            if self.request.method == 'PATCH' or self.request.method == 'PUT':
                self.permission_classes = [IsGroupAdmin, ]
            elif self.request.method == 'POST':
                self.permission_classes = [IsAuthenticated, IsGroupless, ]
            elif self.request.method == 'GET':
                self.permission_classes = [IsGroupMember, ]
            else:
                self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        group = self.get_object()
        members = group.members.all()
        serializer = MembersUserSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = User.objects.get(id=request.user.id) 
        serializer.save(admin=admin)
        admin.group = Group.objects.get(code=serializer.data.get('code'))
        admin.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        group = kwargs.get('pk')
        admin = request.data.get('admin')
        if admin is not None:
            user = User.objects.get(id=admin)
            if user.group_id != group:
                return Response({"detail": "Given admin is not in the group."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)



class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsGroupMember]
        return super().get_permissions()

    def get_queryset(self):
        return Store.objects.filter(group_id=self.kwargs.get('group_pk'))
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_id = self.kwargs.get('group_pk')
        serializer.save(group_id=group_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsGroupMember]
        return super().get_permissions()

    def get_queryset(self):
        group_id = self.kwargs.get('group_pk')
        store_id = self.kwargs.get('store_pk')
        if store_id is not None:
            return Product.objects.filter(group_id=group_id, store_id=store_id)
        return Product.objects.filter(group_id=group_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.user.id
        group = kwargs.get('group_pk')
        store = kwargs.get('store_pk')
        saved = False
        if not store:
            store = request.data.get('store_id')

        if store:
            if Store.objects.filter(id=store).exists():
                serializer.save(store_id=store, group_id=group, added_by_id=user_id)
                saved = True
            else:
                return Response({"detail": "Store not found."}, status=status.HTTP_400_BAD_REQUEST)
        if saved == False:
            serializer.save(group_id=group, added_by_id=user_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)