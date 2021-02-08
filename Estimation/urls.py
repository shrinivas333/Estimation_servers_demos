
from django.urls import path,include
from rest_framework import routers
from .models import User,Item,AddOn,Order
from . import views



router=routers.DefaultRouter()
# router.register('items',views.ItemsViewSet,basename="items")
router.register('addon',views.AddonViewSet,basename="addon")
router.register('users',views.UserViewsets,basename="users")
router.register('items',views.ItemViewsets,basename='items_page')
router.register('orders',views.OrderViewSet,basename='orders_page')




urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]