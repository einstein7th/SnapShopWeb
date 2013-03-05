from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

def home(request):
    return render_to_response("index.html",{},RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

# Not currently used: API functions only used for old iPhone App.
@csrf_exempt
def api(request):
    if request.method == 'GET':
        return HttpResponse('App API page')

    key = request.POST.get('key')
    action = request.POST.get('action')
    data = request.POST.get('data')

    if key != 'Q0a93azJmFYuPpG':
        response = {"success": False, "message": "Invalid API key"}

    elif action == 'register':
        response = api2_register(data)
    elif action == 'login':
        response = api_login(data)
    elif action == 'place_order':
        response = api_place_order(data)
    else:
        response = {"success": False, "message": "Invalid request " + action}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def api_login(data):
    j = simplejson.loads(data)
    email = j.get('email')
    password = j.get('password')
    user = authenticate (username=email, password=password)

    if user is not None:
        return {"success": True, "message": "Login for " + email + " successful!"}
    else:
        return {"success": False, "message": "Login for " + email
              + " failed, invalid username or password."}

def api_place_order(data):
    j = simplejson.loads(data)
    email = j.get('email')
    password = j.get('password')
    user = authenticate (username=email, password=password)

    if user is None:
        return {"success": False, "message": "Login for " + email
              + " failed, invalid username or password."}

    # Charge customer for order
    order = j.get('order')
    payment_info = j.get('charge')

    message_body = simplejson.dumps(j.get('order'))

    # Send email
    send_mail('New SnapShop Order received', message_body, 'admin@snapshop.com',
             ['drpizza.x@gmail.com', 'einstein7th@gmail.com', 'xia.umd@gmail.com'],
             fail_silently = False)

    return {"success": True, "message": "Order sent successfully."}

def api2_register(data):
    # return data
    # print data

    j = simplejson.loads(data)
    email = j.get('email')
    password = j.get('password')
    user = authenticate (username=email, password=password)

    if user is None:
        user = User.objects.create_user(email, email, password) # use email as username
        response = {
            "success": True,
            "message": "User created successfully"
        }

    else:
        response = {
            "success": False,
            "message": "User already exists"
        }

    return response # HttpResponse(simplejson.dumps(response), mimetype='application/json')

def api_register(request):
    if request.method == 'GET':
        return HttpResponse('App register page')

    email = request.POST['email']
    password = request.POST['password']

    reponse = {}

    user = authenticate(username = email, password = password)
    if user is None:
        user = User.objects.create_user(email, email, password) # use email as username
        response = {
            "success": True,
            "message": "User created successfully"
        }

    else:
        response = {
            "success": False,
            "message": "User already exists"
        }

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

