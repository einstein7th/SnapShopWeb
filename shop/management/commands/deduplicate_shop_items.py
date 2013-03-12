from django.core.management.base import BaseCommand, CommandError
from shop.models import ShopItem

class Command(BaseCommand):
    def handle(self, *args, **options):
        shop_items = ShopItem.objects.all().order_by("item_name")
        cur_item = None
        items_to_delete = []
        for item in shop_items:
            if not cur_item:
                cur_item = item
                continue
            if item.item_name==cur_item.item_name:
                items_to_delete.append(item)
            else:
                cur_item = item
            
        map(lambda x: x.delete(),items_to_delete)
