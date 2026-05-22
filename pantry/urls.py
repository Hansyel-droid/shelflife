from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pantry', views.PantryItemViewSet, basename='pantry')
router.register(r'shopping', views.ShoppingListViewSet, basename='shopping')

urlpatterns = [
    path('', include(router.urls)),
]