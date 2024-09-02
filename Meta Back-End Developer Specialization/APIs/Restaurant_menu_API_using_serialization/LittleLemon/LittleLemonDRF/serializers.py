from .models import MenuItem
from rest_framework import serializers
from decimal import Decimal


# using model serializer
class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory']
        extra_kwargs = {
            'price' : { 'min_value' : 2},
            'inventory' : {'min_value': 0}
        }
