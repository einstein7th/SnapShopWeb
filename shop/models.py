from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class ShopItem(models.Model):
    item_category = models.ForeignKey('Categories')
    item_name = models.CharField(max_length = 200)
    item_price = models.IntegerField(default = 99999)
    item_size = models.CharField(max_length=50)
    item_unit_price = models.CharField(max_length=50)
    item_thumb_small = models.CharField(max_length=200)
    item_thumb_medium = models.CharField(max_length=200)
    item_thumb_large = models.CharField(max_length=200)
    item_peapod_productid = models.CharField(max_length=50)
    item_peapod_cnid = models.CharField(max_length=20)
    item_nutrition_html = models.TextField()
    item_description_html = models.TextField()
    item_ingredients_html = models.TextField()
    item_details_html = models.TextField()

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
    category_cnid = models.CharField(max_length=50)
    category_parent = models.ForeignKey('Categories', default=None, null=True)

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

class PurchaseForm(forms.Form):
    DORM_CHOICES = (
        ('362 Memorial Drive', 'Baker House'),
        ('450 Memorial Drive', 'MacGregor House'),
        ('3 Ames Street', 'East Campus'),
        ('460 Beacon Street', 'Nu Delta'),
    )

    EXPIRATION_MONTH_CHOICES = (
        ('1', '01 - January'),
        ('2', '02 - February'),
        ('3', '03 - March'),
        ('4', '04 - April'),
        ('5', '05 - May'),
        ('6', '06 - June'),
        ('7', '07 - July'),
        ('8', '08 - August'),
        ('9', '09 - September'),
        ('10', '10 - October'),
        ('11', '11 - November'),
        ('12', '12 - December'),
    )

    EXPIRATION_YEAR_CHOICES = (
        ('2013', '2013'),
        ('2014', '2014'),
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
    )

    name = forms.CharField(max_length=50, widget=forms.TextInput({'placeholder':'Alyssa P. Hacker'}))
    living_group = forms.ChoiceField(DORM_CHOICES)
    #address_2 = models.CharField(max_length=50)
    #city = models.CharField(max_length=50)
    #state = models.CharField(max_length=50)
    #zip_code = models.CharField(max_length=50)
    card_number = forms.CharField(max_length=16, widget=forms.TextInput({'placeholder':'4012888888881881'}))
    card_cvc = forms.CharField(max_length=4, widget=forms.TextInput({'placeholder':'626'}))
    card_zip = forms.CharField(max_length=5, widget=forms.TextInput({'placeholder':'02139'}))
    card_expiration_month = forms.ChoiceField(EXPIRATION_MONTH_CHOICES)
    card_expiration_year = forms.ChoiceField(EXPIRATION_YEAR_CHOICES)
    promo_code = forms.CharField(required=False, max_length=10) # optional field
    # items_list = forms.TextField(widget=forms.HiddenInput())

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput({'placeholder':'MIT Email', 'class': 'large-input'})
        self.fields['password1'].widget = forms.PasswordInput({'placeholder':'Password', 'class': 'large-input'})
        self.fields['password2'].widget = forms.PasswordInput({'placeholder':'Confirm password', 'class': 'large-input'})

    def is_valid(self, *args, **kwargs):
        return super(RegisterForm, self).is_valid(*args, **kwargs)

    def save(self):
        user = super(RegisterForm, self).save(commit=True)
        user.is_active = True
        user.save()
