
from django.urls import path,include
from rest_framework import routers
from .models import User,Item,AddOn,Order
from . import views
from Estimation.views import ListAddons


router=routers.DefaultRouter()
# router.register('items',views.ItemsViewSet,basename="items")
router.register('addon',views.AddonViewSet,basename="addon")
router.register('users',views.UserViewsets,basename="users")




urlpatterns = [
    path('',include(router.urls)),
    path('items/',ListAddons.as_view()),
    path('items/<int:pk>/',views.ListAddonsDetails.as_view())
  
    
    
]