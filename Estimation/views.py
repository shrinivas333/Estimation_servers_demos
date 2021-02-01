from django.shortcuts import render
from rest_framework.response import Response
from .serializer import CustomerSerializer,AddOnSerializer,ItemSerializer,orderSerializer
from .models import User,AddOn,Item,Order,ItemAddon
from rest_framework import viewsets, mixins,serializers
from django.http import HttpResponse
import json
from rest_framework.views import APIView

# Create your views here.


class ListAddons(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        items=Item.objects.all()
        itemList=[]

        for item in items:
            item_content={}
            item_content['item_id']=item.item_id



            itemAddons=ItemAddon.objects.filter(item=item)
            item_addon_list=[]

            for itemAddon in itemAddons:
                addon_content={}
                addon_content['description'] = itemAddon.item.description
                addon_content['cost'] = itemAddon.item.cost
                addon_content['gst'] = itemAddon.item.gst
                addon_content['material'] = itemAddon.item.material
                addon_content['quantity'] = itemAddon.quantity

                item_addon_list.append(addon_content)
            item_content['addons']=item_addon_list
            itemList.append(item_content)

        return Response(itemList)

class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=CustomerSerializer

class AddonViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    queryset=AddOn.objects.filter()
    serializer_class=AddOnSerializer
    
    

class ItemsViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Item.objects.all()
    serializer_class=ItemSerializer

    def get_items(self,request):

        items=Item.objects.all()
        print(items)
  

    # def get_queryset(self):
        
    #     Items=Item.objects.all()
    #     print(Items)
    #     items_list=[]
    #     addons_list=[]
    #     for item in Items:
    #         print(item.item_id)
    #         print(item.addons.all())
    #         intermdediate=ItemAddon.objects.filter(item=item)
    #         if intermdediate:
    #             print(intermdediate.item)
    #         try :
    #             for addon in item.addons.all():
    #                 quantity =ItemAddon.objects.get(item=item,addon=addon)
    #                 print(quantity)
    #                 addondict={"addon_id":addon.addon_id,"description":addon.description,"cost":addon.cost,"gst":addon.gst,"material":addon.material,"quantity":quantity.quantity}

    #                 addons_list.append(addondict)
    #         except:
    #             addons_list.append(None)
    #         iteminfo={}
    #         iteminfo['item_id']=item.item_id
    #         iteminfo['addons']=addons_list
    #         iteminfo['description']=item.description
    #         iteminfo['cost']=item.cost
    #         iteminfo['gst']=item.gst
    #         iteminfo['material']=item.material

    #         items_list.append(iteminfo)

    #     return HttpResponse(json.dumps(items_list))

    def create(self,request):
        print(request.data)
        item=Item.saveItems(request.data)
        return Response({"Results":str(item)})

