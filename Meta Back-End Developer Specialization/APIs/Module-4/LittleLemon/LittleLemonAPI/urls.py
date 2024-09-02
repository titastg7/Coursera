from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('category/', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),
    path('groups/manager/users/', views.ManagersView.as_view()),
    path('groups/manager/users/<int:pk>/', views.SingleManagerView.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/', views.SingleDeliveryCrewView.as_view()),
    path('cart/menu-items/', views.CartView.as_view()),
]

