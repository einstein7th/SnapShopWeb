from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from django.contrib.auth import *
from django.contrib.auth import login as authLogin
from django.forms.util import ErrorList
from django.http import Http404
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ValidationError
from snapshop.shop.models import PurchaseForm
from snapshop.shop.models import RegisterForm
from snapshop.shop.models import ShopItem
from shop.models import ShopItem, Categories, Customer, CreditCard

import stripe
import json
import datetime

#stripe.api_key = 'sk_test_sdufAGHnjkSHOAO17JLy7mnT' # Test secret key
stripe.api_key = 'sk_live_rytd9V25kvaLa0THdVIlLwae' # Live secret key

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                validate_email(username)
            except ValidationError:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(username + u' is not a valid email address')

            if not username[-7:] == 'mit.edu':
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(username + u' is not an MIT email address')
            else:
                # TODO set email field as username.
                new_user = form.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])

                authLogin(request, new_user)
                return HttpResponseRedirect("/")

    else:
        form = RegisterForm()

    return render_to_response("index.html", {'form': form},
        RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def thanks(request):
    return render_to_response("thanks.html",{},RequestContext(request))

def pretty_price(cents):
    return '$' + str(cents / 100) + '.' + str(cents % 100)

# def currency(dollars):
#    dollars = round(float(dollars), 2)
#    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

# AJAX method to save cart after each change (add/remove item, etc.)
@csrf_exempt
def save_cart(request):
    if request.method == 'POST':
        request.session['cart'] = request.POST['data']
    return render_to_response("thanks.html",{},RequestContext(request))

def results(request):
    if request.method == 'POST': # Submitted the purchase form:
        form = PurchaseForm(request.POST)
        print 'GOT POST'

        if not request.user.is_authenticated():
            errors = form._errors.setdefault("loggedin", ErrorList())
            errors.append("Please log in before ordering")

        elif form.is_valid(): # TODO if form is not valid because no items in cart, say so! item_list is hidden field so user cannot see error.
            hasError = False
            user_email = request.user.username # form.cleaned_data['email']
            email_html = '<p>Name: ' + form.cleaned_data['name'] + '<br />Email: ' + user_email + '<br />Address: ' + form.cleaned_data['living_group'] + '<br />Room number: ' + form.cleaned_data['room_number'] + '<br />Phone number: ' + form.cleaned_data['phone_number'] + '</p><p><b>Delivery date: Sunday, March 17, 2013</b></p><p><b>Order:</b></p>'

            cart_items = json.loads(form.cleaned_data['items_list'])
            cart_total = 0

            print 'cart items: ', cart_items

            for cart_item_id in cart_items:
                # make sure JSON output in cart_item_id form field is int as saved by browser, on chrome is. Otherwise would need to cast.
                qty = cart_items[cart_item_id]
                item = ShopItem.objects.get(pk=cart_item_id)
                cart_total += (item.item_price * qty)
                email_html += '<p>' + str(qty) + 'x ' + item.item_name + ' @ ' + pretty_price(item.item_price) + ' = ' + pretty_price(item.item_price * qty) + ' </p>'


            email_html += '<p>Order total: ' + pretty_price(cart_total) + '</p>'
            # Should also check cart matches the one saved in databse.

            card_dictionary = {
                'number': form.cleaned_data['card_number'],
                'exp_month': form.cleaned_data['card_expiration_month'],
                'exp_year': form.cleaned_data['card_expiration_year'],
                'cvc': form.cleaned_data['card_cvc'],
                'address_zip': form.cleaned_data['card_zip'],
            }

            # process order immediately
            """
            charge = stripe.Charge.create(
                amount=cart_total,
                currency='usd',
                card=card_dictionary,
                description='SnapShop order for ' + form.cleaned_data['name'],
                )
            """

            useCard = False
            if form.cleaned_data['payment_choices'] == 'use_old':
                try:
                    customer = Customer.objects.get(user=request.user)
                    try:
                        card = CreditCard.objects.get(cc_owner=customer)
                        # TODO increase balance from Stripe

                    except CreditCard.DoesNotExist:
                        hasError = True
                        errors = form._errors.setdefault("username", ErrorList())
                        errors.append("An error ocurred in retreiving your saved card. Please re-enter the information below.")

                except Customer.DoesNotExist:
                    hasError = True
                    errors = form._errors.setdefault("username", ErrorList())
                    errors.append("An error ocurred in retreiving your saved card. Please re-enter the information below.")
            else: # payment_choices == 'save_new' or 'no_save'
                # Try only creating customer: should account for customer already created, and save in DB.
                # Catching errors in: https://stripe.com/docs/api?lang=python
                try:
                    stripe_customer = stripe.Customer.create(
                                # use SnapShop username?
                                description="Customer " + form.cleaned_data['name'],
                                card=card_dictionary,
                                account_balance=cart_total,
                                email=user_email, #request.user.username
                            )
                    print stripe_customer
                except stripe.CardError, e:
                    print e
                    errors = form._errors.setdefault("card_number", ErrorList())
                    errors.append("Card error: " + e.message)
                    hasError = True
                except stripe.StripeError, e:
                    print e
                    errors = form._errors.setdefault("card_number", ErrorList())
                    errors.append("A stripe error has ocurred. Please contact the site administrator")
                    hasError = True
                if not hasError:
                    try:
                        our_customer = Customer.objects.get(user=request.user)
                    except Customer.DoesNotExist:
                        our_customer = Customer(stripe_token=stripe_customer.id, phone_number='', delivery_time=datetime.datetime(2013, 03, 16), user=request.user)
                        our_customer.save()

                    # TODO will this create duplicate credit card entries
                    if form.cleaned_data['payment_choices'] == 'save_new':
                        card_number = form.cleaned_data['card_number']
                        our_card = CreditCard(cc_stub=card_number[-4:], cc_type=0, cc_owner=our_customer)
                        our_card.save()

            if not hasError:
                # Send email to us - admins
                admin_msg = EmailMessage('New Snapshop order!', email_html, 'no-reply@snapshopmit.com', ['snapshop@mit.edu', 'drpizza.x@gmail.com'])
                admin_msg.content_subtype = 'html'
                admin_msg.send(fail_silently=False)

                # Senc copy of email to customer
                user_msg = EmailMessage('Thank you for your SnapShop order!', email_html, 'snapshopmit@gmail.com', [user_email])
                user_msg.content_subtype = 'html'
                user_msg.send(fail_silently=True)
                return HttpResponseRedirect('/thanks/')

    NO_CUSTOMER = (
        ('save_new', 'Please remember my card for future orders'),
        ('no_save', "Don't remember my card for future orders"),
    )

    # TODO Cart less janky
    cart_rows = []
    cart_json = ""
    cart_total = 0

    if request.method == 'GET':
        form = PurchaseForm()
        form.fields['payment_choices'].choices = NO_CUSTOMER
        cart_items = []
        try:
            cart_json = request.session['cart']
            cart_items = json.loads(request.session['cart'])
        except KeyError:
            cart_items = []
            cart_json = ""

        cart_total = 0
        cart_rows = []

        try:
            for cart_item_id in cart_items:
                # make sure JSON output in cart_item_id form field is int as saved by browser, on chrome is. Otherwise would need to cast.
                qty = cart_items[cart_item_id]
                item = ShopItem.objects.get(pk=cart_item_id)
                cart_rows.append((qty, item))# send in as tuple of (qty, ShopItem)
                cart_total += (qty * item.item_price)
                # TODO figure out if should simply re-render cart elements in
                # JavaScript rather than having 2 way: template and JS injection
        except TypeError:
            cart_json = ""
            cart_items = []

    if request.user.is_authenticated():
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = None

        if customer is None:
            form.fields['payment_choices'].choices = NO_CUSTOMER
        else:
            cards = CreditCard.objects.filter(cc_owner=customer)
            if len(cards) > 0:
                CARD_EXISTS = (
                    ('use_old', 'Saved card ending in ' + cards[0].cc_stub),
                    ('save_new', 'Please save this new card and use for future orders'),
                    ('no_save', 'Please use the following card and remove my card information'),
                    )
                form.fields['payment_choices'].choices = CARD_EXISTS


    keyword_item_map = {}
    keywords = [k.lower().strip() for k in request.GET.getlist("q")]

    for keyword in keywords:
        keyword_item_map[keyword] = ShopItem.search(keyword)

    return render_to_response("main.html",
                              {'query':", ".join(keywords),
                               'keyword_item_map':keyword_item_map,
                               'form': form,
                               'cart': cart_rows,
                               'cart_json': cart_json,
                               'cart_total': cart_total},
                               RequestContext(request))


def view_item(request,item_id):
    item = get_object_or_404(ShopItem,pk=item_id)
    return render_to_response("item_modal.html",{"item":item},RequestContext(request))
