from rest_framework import serializers
from .models import Order,Item,AddOn,User,ItemAddon,Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = ('customer_id', 'customername', 'phone', 'email','address')
   
class AddonItemSerializer(serializers.ModelSerializer):
    item=serializers.Field(source='item')
    addon=serializers.Field(source='addon')
    class Meta:
        model=ItemAddon
        fields=('item','addon','quantity')

class AddOnSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=AddOn
        fields=('addon_id','description','cost','gst','material',)
        depth=1



class ItemS(serializers.ModelSerializer):
    addons = serializers.SerializerMethodField()

    class Meta:
        model = Item
        # fields ='__all__'
        fields = ('item_id', 'addons','description','cost','gst','material')
        ordering='-user'
        
    def get_addons(self,instance):
        itemAddons = ItemAddon.objects.filter(item=instance)
        item_addon_list = []
        print(itemAddons)
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
    items=ItemS(many=True)
    customer=CustomerSerializer(many=False)
    class Meta:
        model=Order
        fields=('order_id' ,'customer','items','Total','gst','create_date' ,'delivery_date',)



   
