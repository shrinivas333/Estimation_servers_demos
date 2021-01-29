from django.shortcuts import render
from rest_framework.response import Response
from .serializer import CustomerSerializer,AddOnSerializer,ItemSerializer,orderSerializer
from .models import User,AddOn,Item,Order
from rest_framework import viewsets, mixins,serializers
from django.http import JsonResponse
import json
# Create your views here.

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
    queryset = Item.objects.all()
    serializer_class=ItemSerializer

    def create(self,request):
        print(request.data)
        item=Item.saveItems(request.data)
        return Response({"Results":str(item)})

