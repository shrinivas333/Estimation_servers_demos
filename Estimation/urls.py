
from django.urls import path,include
from rest_framework import routers
from .models import User,Item,AddOn,Order
from . import views
from Estimation.views import ListAddons


router=routers.DefaultRouter()
router.register('items',views.ItemsViewSet,basename="items")
router.register('addon',views.AddonViewSet,basename="addon")
router.register('users',views.UserViewsets,basename="users")

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewsets, basename='user')
# router.register(r'addon', views.AddonViewSet, basename='addon')
# urlpatterns = router.urls


urlpatterns = [
    path('',include(router.urls)),
    path('list_addons',ListAddons.as_view())
    
    
]