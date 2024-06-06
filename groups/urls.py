from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from . import views

router = DefaultRouter()
router.register(r'groups', views.GroupViewSet)

groups_nested_router = NestedSimpleRouter(router, r'groups', lookup='group')
groups_nested_router.register(r'products', views.ProductViewSet, basename='group-products')
groups_nested_router.register(r'stores', views.StoreViewSet, basename='group-stores')

stores_nested_router = NestedSimpleRouter(groups_nested_router, r'stores', lookup='store')
stores_nested_router.register(r'products', views.ProductViewSet, basename='store-products')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(groups_nested_router.urls)),
    path('', include(stores_nested_router.urls)),
]
