from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)
    customername=models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, default=None, null=True)
    email = models.EmailField(default=None, null=True, blank=True)
    address = models.CharField(max_length=400, blank=True, default=None, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    @staticmethod
    def addcustomer(data,self):
        print(self.request.user)
        try:
            customer=Customer.objects.get(phone=data['phone'])
            print(customer)
        except:
            customer=None

        if customer is None:
            customer=Customer(customername=data['customername'],phone=data['phone'],email=data['email'],address=data['address'])
            customer.save()
            print(customer)
        return customer

    def __str__(self):
        return self.customername

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
                
                addon=AddOn.objects.get(pk=i['addon_id'])
            except:
                addon=None
           
            if addon is None:
                addon=AddOn(description=i['description'],cost=i['cost'],gst=i['gst'],material=i['material'])
                addon.save()
               
            
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
    user=models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)

    @staticmethod 
    def saveItems(data,self):
        itemList=[]
        print(data)
      
        for item in data:
            i=Item()
            i.description=item['description']
            i.cost=item['cost']
            i.gst=item['gst']
            i.material=item['material']
            i.user=self.request.user
            i.save()
            print(item['addons'])
            addons_quantity_list=item['addons']
        #adding addons to items list
            add_lists=AddOn.addAddons(item['addons'])
            print(add_lists)

            print(addons_quantity_list)
        
            for addon in add_lists:       
                item_addon=ItemAddon(item=i,addon=addon)
                for quant in addons_quantity_list:
                    if addon.addon_id==quant['addon_id']: 
                        print(quant['quantity'])
                        item_addon.quantity = quant['quantity']     
                item_addon.save()
                print(item_addon)
            itemList.append(i)
            print(itemList)   
        return itemList


class ItemAddon(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    addon=models.ForeignKey(AddOn,on_delete=models.CASCADE)
    quantity=models.FloatField(null=True,blank=True)


class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)
    customer=models.ForeignKey(Customer,default=None,null=True, on_delete=models.SET_NULL)
    items=models.ManyToManyField(Item,related_name="orders")
    Total=models.FloatField()
    gst=models.FloatField()
    create_date =models.DateTimeField(auto_now_add=True, null=True)
    delivery_date=models.DateTimeField(null=True,default=None)

    @staticmethod 
    def saveOrders(data,self):
        print(data)
        order=Order()
        order.user=self.request.user
        order.Total=data['Total']
        order.gst=data['gst']
        order.delivery_date=timezone.now()+timezone.timedelta(days=10)
        customer1=Customer.addcustomer(data['customer'],self)
        print(customer1)
        order.customer=customer1
        order.save()

       
        items_lists=Item.saveItems(data['items'],self)
        print(items_lists)
        for item in items_lists:
            order.items.add(item)
        
        return order

