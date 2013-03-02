# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ShopItem(Item):
    # define the fields for your item here like:
    name = Field()
    size = Field()
    unit_price = Field()
    productId = Field()
    price = Field()
    cnid = Field()
    thumb = Field()

class DetailedShopItem(Item):
    # define the fields for your item here like:
    name = Field()
    size = Field()
    unit_price = Field()
    productId = Field()
    price = Field()
    cnid = Field()

    small_image = Field()
    med_image = Field()
    large_image = Field()
    details = Field()
    nutrition = Field()
    ingredients = Field()


class ShopCategory(Item):
    name = Field()
    cnid = Field()
    parent = Field()
    