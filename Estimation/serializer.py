from rest_framework import serializers
from .models import Order,Item,AddOn,User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('user_id', 'username', 'password', 'email')
   
        
class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddOn
        fields=('addon_id','description','cost','gst','material')
        depth=1
        
class ItemSerializer(serializers.ModelSerializer):
    addons=AddOnSerializer(many=True)
    class Meta:
        model=Item
        # fields ='__all__'
        fields=('item_id' ,'addons' ,'description','cost','gst','material')

        

class orderSerializer(serializers.ModelSerializer):
    items=ItemSerializer(many=True)
    class Meta:
        model=Order
        fields=('order_id' ,'customer_id','items','Toatal','gst','create_date' ,'delivery_date','items')