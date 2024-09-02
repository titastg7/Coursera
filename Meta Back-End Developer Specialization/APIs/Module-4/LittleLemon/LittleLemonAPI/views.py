from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, generics, status
from .models import MenuItem, Category, Cart, OrderItem, Order
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer,CartSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import throttle_classes
from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, NotFound


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
    serializer_class = MenuItemSerializer
    ordering_fields=['price']
    search_fields=['title']
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__title__icontains=category)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
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
    

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        current_user = self.request.user
        try:
            order = Order.objects.get(id=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise NotFound("Order does not exist.")
        

        if current_user.groups.filter(name='Manager').exists():
            return order
        elif current_user == order.user :
            return order
        elif current_user.groups.filter(name='DeliveryCrew').exists() and order.delivery_crew == current_user:
            return order
        else:
            raise PermissionDenied("You do not have permission to access this order.")
        
    def update(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise NotFound("Order does not exist.")
        current_user = self.request.user

        if current_user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You do not have permission to update this order.")
    
    def partial_update(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise NotFound("Order does not exist.")
        
        current_user = self.request.user

        if current_user.groups.filter(name='Manager').exists():
            # Manager can update the order
            if 'status' in request.data:
                status_value = request.data['status']
                if status_value == 1 and order.delivery_crew is None :
                    raise PermissionDenied("Order cannot be marked as delivered without an assigned delivery crew.")

            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
        elif current_user.groups.filter(name='DeliveryCrew').exists():
            # Delivery crew can only update the status
            if 'status' in request.data:
                status_value = request.data['status']
                if status_value == 1 and order.delivery_crew is None:
                    raise PermissionDenied("Order cannot be marked as delivered without an assigned delivery crew.")

                serializer = self.get_serializer(order, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                raise PermissionDenied("You can only update the status of the order.")
        else:
            raise PermissionDenied("You do not have permission to update this order.")
        
    def destroy(self, request, *args, **kwargs):
        current_user = self.request.user
        try:
            order = Order.objects.get(id=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise NotFound("Order does not exist.")
        
        if current_user.groups.filter(name='Manager').exists():
            self.perform_destroy(order)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You do not have permission to delete this order.")

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        orders = self.get_queryset()
        order_serializer = self.get_serializer(orders, many=True)
        return Response(order_serializer.data)
        
    def create(self, request, *args, **kwargs):
        current_user = request.user

        cart_items = Cart.objects.filter(user=current_user)
        if cart_items.count() == 0:
            return Response({"Message:": "No item in cart"})

        total_price = sum(item.price for item in cart_items)

        # create order
        order_data = {'user' : current_user.id,'total': total_price, 'date': timezone.now().date()}
        order_serializer = self.get_serializer(data=order_data)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()
        
        order_items = []
        for cart_item in cart_items:
            order_item_data = {
                'order': order.id,
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            }
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()
            order_items.append(order_item_serializer.data)

        # Step 4: Delete cart items
        cart_items.delete()

        response_data = {
            'order': order_serializer.data,
            'order_items': order_items
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
