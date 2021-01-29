from django.contrib import admin
from .models import User,AddOn,Item,Order,ItemAddon
# Register your models here.

admin.site.register(User)
admin.site.register(AddOn)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(ItemAddon)