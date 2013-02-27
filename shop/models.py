from django.db import models

# Create your models here.

class shipping_label(models.Model):
	address_first_line = models.CharField(max_length=50)
	address_second_line = models.CharField(max_length=50)
	address_zip_code = models.IntegerField()
	address_city = models.CharField(max_length=50)
	address_state = models.CharField(max_length=2)
	owner = models.OneToOneField(customer)

class credit_card(models.Model):
	cc_stub = models.CharField(max_length=4, default="****")

class categories(models.Model):
	category_name = models.CharField(max_length=50)

class item(models.Model):
	item_name = models.CharField(max_length = 50)
	item_price = models.IntegerField(efault = 99999)
	item_size = models.CharField(max_length=50)
	item_qty = models.IntegerField(default=0)

class shopping_cart(models.Model):
	items = models.ForeignKey(item)
	owner = models.OneToOneField(customer)

class customer(models.Model):
	current_shipping_addr = models.ForeignKey(shipping_label)
	current_creditcard = models.OneToOneField(credit_card)
	stripe_token = models.CharField(max_length=20)
	cart = models.OneToOneField(shopping_cart)
	phone_number = models.CharField(max_length=20)
	delivery_time = models.DateTimeField()
	user = models.OneToOneField(User, primary_key=True)