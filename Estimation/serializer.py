from rest_framework import serializers
from .models import Order,Item,AddOn,User,ItemAddon


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('user_id', 'username', 'password', 'email')
   
class AddonItemSerializer(serializers.ModelSerializer):
    item=serializers.Field(source='item')
    addon=serializers.Field(source='addon')
    class Meta:
        model=ItemAddon
        fields=('item','addon','quantity')

class AddOnSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    class Meta:
        model=AddOn
        fields=('addon_id','description','cost','gst','material','quantity')
        depth=1

    def get_quantity(self,instance):
        print(instance)
        item_addons=ItemAddon.objects.filter(addon=instance)
        # tem_addon=ItemAddon.objects.filter(addon=instance)
        # print(tem_addon)
    #     return item_addon.quantity
        

class ItemSerializer(serializers.ModelSerializer):
    addons=AddOnSerializer(many=True,)
    class Meta:
        model=Item
        # fields ='__all__'
        fields=('item_id' ,'addons' ,'description','cost','gst','material')

        

class orderSerializer(serializers.ModelSerializer):
    items=ItemSerializer(many=True)
    class Meta:
        model=Order
        fields=('order_id' ,'customer_id','items','Toatal','gst','create_date' ,'delivery_date','items')