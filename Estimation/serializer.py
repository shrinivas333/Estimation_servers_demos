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
        # item_addons=ItemAddon.objects.filter(addon=instance)
        # print(item_addons)
        # tem_addon=ItemAddon.objects.filter(addon=instance)
        # print(tem_addon)
    #     return item_addon.quantity
        

class ItemSerializer(serializers.ModelSerializer):
    addons=AddOnSerializer(many=True,)
 
    class Meta:
        model=Item
        # fields ='__all__'
        fields=('item_id' ,'addons' ,'description','cost','gst','material')


class ItemS(serializers.ModelSerializer):
    addons = serializers.SerializerMethodField()

    class Meta:
        model = Item
        # fields ='__all__'
        fields = ('item_id', 'addons')

    def get_addons(self,instance):
        itemAddons = ItemAddon.objects.filter(item=instance)
        item_addon_list = []

        for itemAddon in itemAddons:
            addon_content = {}
            addon_content['addon_id'] = itemAddon.addon.addon_id
            addon_content['description'] = itemAddon.addon.description
            addon_content['cost'] = itemAddon.addon.cost
            addon_content['gst'] = itemAddon.addon.gst
            addon_content['material'] = itemAddon.addon.material
            addon_content['quantity'] = itemAddon.quantity

            item_addon_list.append(addon_content)
        return item_addon_list

class orderSerializer(serializers.ModelSerializer):
    items=ItemSerializer(many=True)
    class Meta:
        model=Order
        fields=('order_id' ,'customer_id','items','Toatal','gst','create_date' ,'delivery_date','items')