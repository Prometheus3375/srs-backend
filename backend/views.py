from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.contrib.sessions.backends.base import SessionBase
import json


def index(request: HttpRequest):
    session: SessionBase = request.session
    print(f"Remote IP: {request.META['REMOTE_ADDR']}")
    if request.method == 'GET':
        session['data'] = []
        return HttpResponse('This is main page')
    if request.method == 'POST':
        print(request.POST)
        # session.cycle_key()
        with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        session['data'] = data
        return HttpResponse('This is main page')
    else:
        print(f'{session} sent {request.method} request')
        return HttpResponseBadRequest()


def results(request: HttpRequest):
    session: SessionBase = request.session
    if request.method == 'GET':
        data = session['data']
        return HttpResponse(json.dumps(data), content_type = 'application/json')
    else:
        print(f'{session} sent {request.method} request')
        return HttpResponseBadRequest()


# @api_view(['GET', 'POST'])
# def index(request: Request):
#     session: SessionBase = request.session
#     if request.method == 'GET':
#         session['data'] = []
#         return Response()
#     elif request.method == 'POST':
#         print(request.POST)
#         with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
#             data = json.load(f)
#         session['data'] = data
#         return Response(data)
#
#
# @api_view(['GET'])
# def results(request: Request):
#     session: SessionBase = request.session
#     data = session['data']
#     return Response(data)
