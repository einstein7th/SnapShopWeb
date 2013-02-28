from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ShippingLabel(models.Model):
	address_first_line = models.CharField(max_length=50)
	address_second_line = models.CharField(max_length=50)
	address_zip_code = models.IntegerField()
	address_city = models.CharField(max_length=50)
	address_state = models.CharField(max_length=2)

class CreditCard(models.Model):
	cc_stub = models.CharField(max_length=4, default="****")
	cc_type = models.IntegerField() 

class Categories(models.Model):
	category_thumb = models.CharField(max_length=200)
	category_name = models.CharField(max_length=50)

class Item(models.Model):
	item_name = models.CharField(max_length = 50)
	item_price = models.IntegerField(default = 99999)
	item_size = models.CharField(max_length=50)
	item_qty = models.IntegerField(default=0)
	item_thumb = models.CharField(max_length=200)

class ShoppingCart(models.Model):
	items = models.ForeignKey(Item)

class Customer(models.Model):
	current_shipping_addr = models.ForeignKey(ShippingLabel)
	current_creditcard = models.OneToOneField(CreditCard)
	stripe_token = models.CharField(max_length=20)
	cart = models.OneToOneField(ShoppingCart)
	phone_number = models.CharField(max_length=20)
	delivery_time = models.DateTimeField()
	user = models.OneToOneField(User)