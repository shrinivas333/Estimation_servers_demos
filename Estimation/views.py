from django.shortcuts import render
from rest_framework.response import Response
from .serializer import CustomerSerializer,AddOnSerializer,orderSerializer,ItemS
from .models import User,AddOn,Item,Order,ItemAddon,Customer
from rest_framework import viewsets, mixins,serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import BasePagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Estimation_server_demo.pagination import CustomPagination
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ItemViewsets(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class= ItemS
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['description',]

    def get_queryset(self):
        print(self.request.user)
        return Item.objects.filter(user=self.request.user)

    def create(self,request):
        print(request.data)
        item=Item.saveItems(request.data,self)
        return Response({"Results":str(item)})


class UserViewsets(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    pagination_class = StandardResultsSetPagination
    # filter_backends = [filters.SearchFilter]
    filter_fields = ('phone','customername')

class AddonViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    queryset=AddOn.objects.filter()
    serializer_class=AddOnSerializer
    
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class= orderSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return Order.objects.filter(user=self.request.user)
    
    def create(self,request):
        order=Order.saveOrders(request.data,self)
        return Response({"Results":str(order)})