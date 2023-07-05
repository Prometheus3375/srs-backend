from django.http import HttpResponse
from django.shortcuts import render
import json


def index(request):
    return HttpResponse('This is main page')


# def results(request, data):
#     data = json.loads(data)
def results(request):
    data = [
        {
            'name': 'Super notebook',
            'price': '1000$',
            'sites': ['amazon', 'e-bay'],
        },
        {
            'name': 'Not a super notebook',
            'price': '10$',
            'sites': ['amazon', 'e-bay'],
        },
    ]
    return HttpResponse(json.dumps(data))
