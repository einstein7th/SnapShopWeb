from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response("index.html",{},RequestContext(request))

def search(request):
    return render_to_response("search.html",{},RequestContext(request))

def main(request):
    query = request.GET.get("q","")
    return render_to_response("main.html",
                              {'query':query},
                              RequestContext(request))
