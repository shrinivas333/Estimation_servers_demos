from django.shortcuts import render
from rest_framework.response import Response
from .serializer import CustomerSerializer,AddOnSerializer,ItemSerializer,orderSerializer
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
# Create your views here.

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ListAddons(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPagination
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
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

