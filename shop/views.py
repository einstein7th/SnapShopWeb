from django.shortcuts import render_to_response
from django.template import RequestContext
from shop.models import ShopItem, Categories

def sign_up(request):
    return render_to_response("index.html",{},RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def results(request):
    query = request.GET.get("q","")
    keyword_item_map = {}
    for keyword in query.split(" "):
        possible_items = ShopItem.objects.filter(item_name__icontains=keyword)
        categories = Categories.objects.filter(category_name__icontains=keyword)
        if categories:
            possible_items.filter(item_category=categories[0])
        keyword_item_map[keyword] = possible_items[:5]

    return render_to_response("main.html",
                              {'query':query,
                               'keyword_item_map':keyword_item_map},
                              RequestContext(request))
