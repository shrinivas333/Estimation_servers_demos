from django.db import models

# Create your models here.

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=30)
    email=models.EmailField()

    def __str__(self):
        return self.username

class AddOn(models.Model):
    GOLD = 0;
    SILVER = 1;
    MATERIAL_CHOICE = ((GOLD, "Gold"), (SILVER, "Silvers"))

    addon_id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=150,unique=True)
    cost=models.FloatField()
    gst=models.FloatField()
    material=models.SmallIntegerField(choices=MATERIAL_CHOICE,default=GOLD)

    @staticmethod
    def addAddons(data):
        print(data)
        addons_list=[]
        for i in data:
            try:
                print(i['description'])
                addon=AddOn.objects.get(description__icontains=i['description'])
            except:
                addon=None
            print('from table')
            print(addon)
            if addon is None:
                addon=AddOn(description=i['description'],cost=i['cost'],gst=i['gst'],material=i['material'])
                addon.save()
                print('from frontend')
                print(addon)
            
            addons_list.append(addon)
        return addons_list

    
    @staticmethod
    def saveAddons(data):
        addons=AddOn(**data)
        addons.save()
        return addons


   

class Item(models.Model):
    GOLD = 0;
    SILVER = 1;
    MATERIAL_CHOICE = ((GOLD, "Gold"), (SILVER, "Silvers"))

    item_id=models.AutoField(primary_key=True)
    addons=models.ManyToManyField(AddOn,related_name="items" ,through="ItemAddon")
    description=models.CharField(max_length=150,null=True,default=None,blank=True)
    cost=models.FloatField()
    gst=models.FloatField(null=True,blank=True)
    material=models.SmallIntegerField(choices=MATERIAL_CHOICE,default=GOLD)

    @staticmethod 
    def saveItems(data):
        print(data)
        item=Item()
        item.description=data['description']
        item.cost=data['cost']
        item.gst=data['gst']
        item.material=data['material']
        item.save()

    #adding addons to items list
        add_lists=AddOn.addAddons(data['addons'])
        print(add_lists)
        for add_list in add_lists:
            item.addons.add(add_list)  

        return item


class ItemAddon(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    addon=models.ForeignKey(AddOn,on_delete=models.CASCADE)
    quantity=models.FloatField()


class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(User,default=None,null=True, on_delete=models.SET_NULL)
    items=models.ManyToManyField(Item,related_name="orders")
    Total=models.FloatField()
    gst=models.FloatField()
    create_date =models.DateTimeField(auto_now_add=True, null=True)
    delivery_date=models.DateTimeField(null=True,default=None)

