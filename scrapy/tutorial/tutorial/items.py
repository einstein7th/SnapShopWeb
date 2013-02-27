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
    cnid = Field()

class ShopCategory(Item):
    name = Field()
    cnid = Field()
    parent = Field()
    