from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from shop.models import ShopItem, Categories
from django.shortcuts import HttpResponseRedirect
from snapshop.shop.models import PurchaseForm
from snapshop.shop.models import RegisterForm
from django.contrib.auth.models import User
from django.forms.util import ErrorList

import stripe

from django.contrib.auth import *                                       # django.contrib.auth.login is internal method used to log in user
from django.contrib.auth import login as authLogin
from django.contrib.auth.views import login             # django.contrib.auth.views.login renders /accounts/login.html view

stripe.api_key = 'sk_test_sdufAGHnjkSHOAO17JLy7mnT' # Test secret key
# 'sk_live_rytd9V25kvaLa0THdVIlLwae' # Live secret key

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            if not 'mit.edu' in username:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(username + u' is not a valid MIT email address')
                # can also use in place of username:
                # django.forms.forms.NON_FIELD_ERRORS
            else:
                new_user = form.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])

                authLogin(request, new_user)
                return HttpResponseRedirect("/search/")

    else:
        form = RegisterForm()

    return render_to_response("index.html", {'form': form},
        RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def thanks(request):
    return render_to_response("thanks.html",{},RequestContext(request))

# def main(request):
#     if request.method == 'POST': # Submitted the purchase form:
#         form = PurchaseForm(request.POST)
#         print 'checking form validity'

#         if form.is_valid():
#             card_dictionary = {
#                 'number': form.cleaned_data['card_number'],
#                 'exp_month': form.cleaned_data['card_expiration_month'],
#                 'exp_year': form.cleaned_data['card_expiration_year'],
#                 'cvc': form.cleaned_data['card_cvc'],
#                 'address_zip': form.cleaned_data['card_zip'],
#             }

#             # process order
#             charge = stripe.Charge.create(
#                 amount=1337,
#                 currency='usd',
#                 card=card_dictionary,
#                 description='SnapShop order for ' + form.cleaned_data['name'],
#                 )

#             # Try only creating customer:
#             customer = stripe.Customer.create(
#                 # use SnapShop username?
#                 description="Customer " + form.cleaned_data['name'],
#                 card=card_dictionary,
#                 account_balance=1337,
#                 )

#             print charge

#             if charge.paid: # if succeeds then we go to thank you page
#                 # send email
#                 return HttpResponseRedirect('/thanks/')

#             # if invalid proceeds below, and re-displays form showing errors
#             else:
#                 form.errors = c.failure_message

#     else:
#         form = PurchaseForm()

#     query = request.GET.get("q","")
#     keywords = query.split(" ") if query else None

#     return render_to_response("main.html",
#                               {'query': query,
#                                'keywords': keywords,
#                                'form': form},

def results(request):
    if request.method == 'POST': # Submitted the purchase form:
        form = PurchaseForm(request.POST)
        print 'checking form validity'

        if form.is_valid():
            card_dictionary = {
                'number': form.cleaned_data['card_number'],
                'exp_month': form.cleaned_data['card_expiration_month'],
                'exp_year': form.cleaned_data['card_expiration_year'],
                'cvc': form.cleaned_data['card_cvc'],
                'address_zip': form.cleaned_data['card_zip'],
            }

            # process order
            charge = stripe.Charge.create(
                amount=1337,
                currency='usd',
                card=card_dictionary,
                description='SnapShop order for ' + form.cleaned_data['name'],
                )

            # Try only creating customer:
            customer = stripe.Customer.create(
                # use SnapShop username?
                description="Customer " + form.cleaned_data['name'],
                card=card_dictionary,
                account_balance=1337,
                )

            print charge

            if charge.paid: # if succeeds then we go to thank you page
                # send email
                return HttpResponseRedirect('/thanks/')

            # if invalid proceeds below, and re-displays form showing errors
            else:
                form.errors = c.failure_message

    else:
        form = PurchaseForm()


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
                               'keyword_item_map':keyword_item_map,
                               'form': form},
                              RequestContext(request))
