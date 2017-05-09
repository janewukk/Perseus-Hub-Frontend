from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.

def egonet(request):
    print 'egonet request'
    with open('app/static/js/egonet.json') as json_file:
        json_data = json_file.read()
        obj = json.loads(json_data)
    return JsonResponse(obj)
