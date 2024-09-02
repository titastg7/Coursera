from .models import MenuItem
from rest_framework import serializers
from .models import Category, Cart, Order, OrderItem
from django.contrib.auth.models import User

# Relationship Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name', 'last_name']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()    
        )
    
    def validate(self, attrs):
        attrs["price"] = attrs["quantity"] * attrs["unit_price"]
        return attrs
    
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price','quantity','price']
        extra_kwargs = {"price": {"read_only": True}}

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order", "menuitem", "unit_price", "quantity","price"]


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set  = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "delivery_crew", "status", "total", "date", "orderitem_set"]
