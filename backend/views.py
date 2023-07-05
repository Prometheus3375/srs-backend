from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.contrib.sessions.backends.base import SessionBase
import json


@api_view(['GET', 'POST'])
def index(request: Request):
    session: SessionBase = request.session
    if request.method == 'GET':
        session['data'] = []
        return Response()
    elif request.method == 'POST':
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
        session['data'] = data
        return Response(data)


@api_view(['GET'])
def results(request: Request):
    session: SessionBase = request.session
    data = session['data']
    return Response(data)

# def index(request: HttpRequest):
#     session: SessionBase = request.session
#     if request.method == 'POST':
#         # session.cycle_key()
#         data = [
#             {
#                 'name': 'Super notebook',
#                 'price': '1000$',
#                 'sites': ['amazon', 'e-bay'],
#             },
#             {
#                 'name': 'Not a super notebook',
#                 'price': '10$',
#                 'sites': ['amazon', 'e-bay'],
#             },
#         ]
#         session['data'] = data
#         return HttpResponse('This is main page')
#     else:
#         print(f'{session} sent {request.method} request')
#         return HttpResponseBadRequest()


# def results(request: HttpRequest):
#     session: SessionBase = request.session
#     if request.method == 'GET':
#         data = session['data']
#         return HttpResponse(json.dumps(data))
#     else:
#         print(f'{session} sent {request.method} request')
#         return HttpResponseBadRequest()
