from rest_framework import permissions, viewsets, generics, status
from .models import MenuItem, Category, Cart, OrderItem, Order
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer,CartSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, throttle_classes
from django.contrib.auth.models import User, Group

class IsManager(permissions.BasePermission):
    def has_permission(self, request,view):
        return request.user and request.user.groups.filter(name='Manager').exists()
    
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields=['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            permission_classes = [IsAuthenticated,IsAdminUser]
            return [permission() for permission in permission_classes]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price']
    search_fields=['category__title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            permission_classes = [IsAuthenticated,IsManager]
            return [permission() for permission in permission_classes]
        
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class  = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            permission_classes = [IsAuthenticated,IsManager]
            return [permission() for permission in permission_classes]
        
class SingleManagerView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        manager_group = Group.objects.get(name='Manager')
        instance.groups.remove(manager_group)
        instance.save()

class ManagersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        manager_group = Group.objects.get(name='Manager')
        user.groups.add(manager_group)

class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.filter(groups__name='DeliveryCrew')
    serializer_class = UserSerializer
    
    
    def perform_destroy(self, instance):
        delivery_crew_group = Group.objects.get(name='DeliveryCrew')
        instance.groups.remove(delivery_crew_group)
        instance.save()

class DeliveryCrewView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.filter(groups__name='DeliveryCrew')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        delivery_crew_group = Group.objects.get(name='DeliveryCrew')
        user.groups.add(delivery_crew_group)


class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response({'detail': 'All items removed from cart'}, status=status.HTTP_204_NO_CONTENT)

'''
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if (
            self.request.user.groups.count() == 0
        ):  # Normal user, not belonging to any group = Customer
            return Response("Not Ok")
        else:  # everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)
'''