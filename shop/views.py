from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response("index.html",{},RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def main(request):
    return render_to_response("main.html",{},RequestContext(request))
