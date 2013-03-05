from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from snapshop.shop.models import PurchaseForm
import stripe

stripe.api_key = 'sk_test_sdufAGHnjkSHOAO17JLy7mnT' # Test secret key
# 'sk_live_rytd9V25kvaLa0THdVIlLwae' # Live secret key

def index(request):
    return render_to_response("index.html",{},RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def thanks(request):
    return render_to_response("thanks.html",{},RequestContext(request))

def main(request):
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
                description="Customer " + form.cleaned_data['name'], # use SnapShop username? 
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
    keywords = query.split(" ") if query else None

    return render_to_response("main.html",
                              {'query': query,
                               'keywords': keywords,
                               'form': form},
                              RequestContext(request))

def purchase(request):
    form = PurchaseForm()
    return render(request, "purchase.html",
                              {'form': form, }
                              )