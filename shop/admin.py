from django.contrib import admin
from shop.models import (ShopItem,
                         ShippingLabel,
                         CreditCard,
                         Categories,
                         CartItem,
                         ShoppingCart,
                         Customer)

class ShopItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(ShopItem, ShopItemAdmin)

class ShippingLabelAdmin(admin.ModelAdmin):
    pass
admin.site.register(ShippingLabel, ShippingLabelAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    pass
admin.site.register(CreditCard, CreditCardAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Categories, CategoriesAdmin)

class CartItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CartItem, CartItemAdmin)

class ShoppingCartAdmin(admin.ModelAdmin):
    pass
admin.site.register(ShoppingCart, ShoppingCartAdmin)

class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)
