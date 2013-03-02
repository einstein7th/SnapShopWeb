from django.db import models
from django.contrib.auth.models import User

class ShopItem(models.Model):
	item_category = models.ForeignKey('Categories')
	item_name = models.CharField(max_length = 50)
	item_price = models.IntegerField(default = 99999)
	item_size = models.CharField(max_length=50)
	item_thumb_small = models.CharField(max_length=200)
	item_thumb_large = models.CharField(max_length=200)
	# item_nutrition_html = models.CharField()
	# item_description_html
	# item_ingredients_html

class ShippingLabel(models.Model):
	address_first_line = models.CharField(max_length=50)
	address_second_line = models.CharField(max_length=50)
	address_zip_code = models.IntegerField()
	address_city = models.CharField(max_length=50)
	address_state = models.CharField(max_length=2)
	address_owner = models.ForeignKey('Customer')

class CreditCard(models.Model):
	cc_stub = models.CharField(max_length=4, default="****")
	cc_type = models.IntegerField() 
	cc_owner = models.ForeignKey('Customer')

class Categories(models.Model):
	category_thumb = models.CharField(max_length=200)
	category_name = models.CharField(max_length=50)

class CartItem(models.Model):
	shop_item_ref = models.ForeignKey(ShopItem)
	cart = models.ForeignKey('ShoppingCart')
	cart_item_qty = models.IntegerField(default=0)
	
class ShoppingCart(models.Model):
	cart_owner = models.OneToOneField('Customer')

class Customer(models.Model):
	stripe_token = models.CharField(max_length=20)
	phone_number = models.CharField(max_length=20)
	delivery_time = models.DateTimeField()
	user = models.OneToOneField(User)