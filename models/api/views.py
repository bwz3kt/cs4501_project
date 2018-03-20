from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import os
import hmac
from django.conf import settings
from django.contrib.auth.hashers import *


@csrf_exempt
def get_list(request):
    apts = Apartment.objects.all().values()
    data = {}
    data['valid'] = True
    data['result'] = list(apts)
    ids = {}
    if len(Apartment.objects.all()) > 0:
        ids['id'] = list(apts)[0].get('id')
    for i in range(len(data['result'])):
        data['result'][i]['id'] = list(apts)[i].get('id')
    return JsonResponse(data)

@csrf_exempt
def get_top_list(request):
    apts = Apartment.objects.all().order_by('-rating')[:5].values()
    data = {}
    data['valid'] = True
    data['result'] = list(apts)
    ids = {}
    if len(Apartment.objects.all()) > 0:
        ids['id'] = list(apts)[0].get('id')
    for i in range(len(data['result'])):
        data['result'][i]['id'] = list(apts)[i].get('id')
    return JsonResponse(data)

@csrf_exempt
def get_price_list(request):
    apts = Apartment.objects.all().order_by('price')[:5].values()
    data = {}
    data['valid'] = True
    data['result'] = list(apts)
    ids = {}
    if len(Apartment.objects.all()) > 0:
        ids['id'] = list(apts)[0].get('id')
    for i in range(len(data['result'])):
        data['result'][i]['id'] = list(apts)[i].get('id')
    return JsonResponse(data)

@csrf_exempt
def item(request, id):
    data = {}
    if Apartment.objects.all().filter(id=id).exists():
        apts = Apartment.objects.all().filter(id=id).values()
        data = {}
        data['valid'] = True
        data['result'] = list(apts)
        data['result'][0]['id'] = id
        print(data['result'])
    else:
        data['valid'] = False
        data['message'] = 'Apartment does not exist.'
    return JsonResponse(data)

@csrf_exempt
def signup(request):
    data = {}
    if request.method == "POST":
        if User.objects.all().filter(username=request.POST.get('username')).exists():
            data['valid'] = False
            data['message'] = 'Username already exists.'
        elif User.objects.all().filter(email=request.POST.get('email')).exists():
            data['valid'] = False
            data['message'] = "Email already has an associated account."
        else:
            user = User()
            user.username = request.POST.get('username')
            user.password = request.POST.get('password')
            user.email = request.POST.get('email')
            user.save()

            authenticator = Authenticator()
            authenticator_value = hmac.new(
                key=settings.SECRET_KEY.encode('utf-8'),
                msg=os.urandom(32),
                digestmod='sha256',
            ).hexdigest()
            authenticator.authenticator = authenticator_value
            authenticator.user_id = user.id
            authenticator.save()

            jsondata = [{
                "username": user.username,
                'id': user.id
            }]
            data['valid'] = True
            data['message'] = 'Created new User.'
            data['result'] = jsondata
            data['authenticator'] = authenticator_value
    else:
        data['valid'] = False
        data['message'] = 'Not a POST request.'
    return JsonResponse(data)

@csrf_exempt
def login(request):
    data = {}
    if request.method == "POST":
        if not (User.objects.all().filter(username=request.POST.get('username')).exists()):
            data['valid'] = False
            data['message'] = 'Username does not exist.'
        else:
            user = User.objects.get(username=request.POST.get('username'))
            if check_password(request.POST.get('password'), user.password):
                authenticator = Authenticator()
                authenticator_value = hmac.new(
                    key=settings.SECRET_KEY.encode('utf-8'),
                    msg=os.urandom(32),
                    digestmod='sha256',
                ).hexdigest()
                authenticator.authenticator = authenticator_value
                authenticator.user_id = user.id
                authenticator.save()

                jsondata = [{
                    "username": user.username,
                    'id': user.id
                }]
                data['valid'] = True
                data['message'] = 'User authenticated.'
                data['result'] = jsondata
                data['authenticator'] = authenticator_value
            else:
                data['valid'] = False
                data['message'] = 'Password incorrect.'
    else:
        data['valid'] = False
        data['message'] = 'Not a POST request.'
    return JsonResponse(data)

@csrf_exempt
def logout(request):
    data = {}
    if not (Authenticator.objects.all().filter(authenticator=request.POST.get('auth')).exists()):
        data['valid'] = False
        data['message'] = 'Authenticator does not exist.'
    else:
        auth = Authenticator.objects.get(authenticator=request.POST.get('auth'))
        auth.delete()
        data['valid'] = True
        data['message'] = 'Authenticator removed successfully';
    return JsonResponse(data)

@csrf_exempt
def delete(request, id):
    data = {}
    if request.method == "GET":
        if Apartment.objects.all().filter(id=id).exists():
            apt = Apartment.objects.get(id=id)
            apt.delete()
            data['valid'] = True
            data['message'] = 'Apartment deleted.'
        else:
            data['valid'] = False
            data['message'] = 'Apartment does not exist.'
    else:
        data['valid'] = False
        data['message'] = 'Not a GET request.'
    return JsonResponse(data)


@csrf_exempt
def create(request):
    data = {}
    if request.method == "POST":
        apt = Apartment()
        apt.name = request.POST.get('name', "")
        apt.price = request.POST.get('price', "")
        apt.save()
        jsondata = [{
            "name": apt.name,
            'id': apt.id,
            'price': apt.price,
        }]
        data['valid'] = True
        data['message'] = 'Created new Apartment.'
        data['result'] = jsondata
    else:
        data['valid'] = False
        data['message'] = 'Not a POST request.'
    return JsonResponse(data)

@csrf_exempt
def update(request, id):
    data = {}
    if request.method == "POST":
        apt = Apartment()
        apt.id = id
        apt.name = request.POST.get('name')
        apt.price = request.POST.get('price')
        apt.save()
        jsondata = [{
            "name": apt.name,
            'id': apt.id,
            'price': apt.price,
        }]
        data['valid'] = True
        data['message'] = 'Updated the Apartment.'
        data['result'] = jsondata
    else:
        data['valid'] = False
        data['message'] = 'Not a POST request.'
    return JsonResponse(data)
