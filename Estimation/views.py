from django.shortcuts import render
from rest_framework.response import Response
from .serializer import CustomerSerializer,AddOnSerializer,ItemSerializer,orderSerializer,ItemS
from .models import User,AddOn,Item,Order,ItemAddon
from rest_framework import viewsets, mixins,serializers
from django.http import HttpResponse
import json
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import BasePagination
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Estimation_server_demo.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .customview import CustomApiView
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ItemViewsets(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class= ItemS
    pagination_class = StandardResultsSetPagination




class ListAddons(CustomApiView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    serializer_class=ItemSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print(self.request.user)
        
        items=Item.objects.filter()
        itemList=[]

        for item in items:
            item_content={}
            item_content['item_id']=item.item_id
            


            itemAddons=ItemAddon.objects.filter(item=item)
            item_addon_list=[]

            for itemAddon in itemAddons:
                addon_content={}
                addon_content['addon_id']=itemAddon.addon.addon_id
                addon_content['description'] = itemAddon.addon.description
                addon_content['cost'] = itemAddon.addon.cost
                addon_content['gst'] = itemAddon.addon.gst
                addon_content['material'] = itemAddon.addon.material
                addon_content['quantity'] = itemAddon.quantity

                item_addon_list.append(addon_content)

            item_content['addons']=item_addon_list
            item_content['description']=item.description
            item_content['cost']=item.cost
            item_content['gst']=item.gst
            item_content['material']=item.material
            itemList.append(item_content)

    
        

        return Response(itemList)


    def post(self,request):
        print(request.data)
        item=Item.saveItems(request.data)
        return Response({"Results":item})     

class ListAddonsDetails(APIView):
        '''
            Retrive, delete and patch operations for  items 
        '''
        permission_classes = [IsAuthenticated]
        def get(self ,request,pk,format=None):
            try:
                item=Item.objects.get(pk=pk)
                print(item)
                item_content={}
                item_content['item_id']=item.item_id
                

                itemAddons=ItemAddon.objects.filter(item=item)
                item_addon_list=[]
                for itemAddon in itemAddons:
                    addon_content={}
                    addon_content['addon_id']=itemAddon.addon.addon_id
                    addon_content['description'] = itemAddon.addon.description
                    addon_content['cost'] = itemAddon.addon.cost
                    addon_content['gst'] = itemAddon.addon.gst
                    addon_content['material'] = itemAddon.addon.material
                    addon_content['quantity'] = itemAddon.quantity

                    item_addon_list.append(addon_content)
                item_content['addons']=item_addon_list
                item_content['description']=item.description
                item_content['cost']=item.cost
                item_content['gst']=item.gst
                item_content['material']=item.material

                return Response(item_content)

            except item.DoesNotExist:
                raise Http404


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
    
    

class ItemsViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    pagination_class=CustomPagination
    queryset = Item.objects.all()
    serializer_class=ItemSerializer

   
  
    def create(self,request):
        print(request.data)
        item=Item.saveItems(request.data)
        return Response({"Results":str(item)})

