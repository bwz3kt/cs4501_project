from django.http import JsonResponse
import json
import urllib.request
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import hashers
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import *


@csrf_exempt
def get_data(request):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/list/')
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)['result']

    return JsonResponse({'results':response})

@csrf_exempt
def get_top_data(request):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/top_list/')
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)['result']

    return JsonResponse({'results':response})

@csrf_exempt
def get_price_data(request):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/price_list/')
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)['result']

    return JsonResponse({'results':response})

@csrf_exempt
def get_details(request, id):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/item/' + str(id))
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)['result']

    return JsonResponse({'result':response})

@csrf_exempt
def create(request):
    post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price")}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/create/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)['message']
    return JsonResponse({'result': response})

@csrf_exempt
def signup(request):
    if request.POST.get("password") == request.POST.get("passwordConfirm"):
        password = make_password(request.POST.get("password"))
        post_data = {'username': request.POST.get("username"), 'email': request.POST.get("email"),
                     'password': password}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/signup/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        response = json.loads(resp_json)
    else:
        return JsonResponse({'valid': False, 'result': "Passwords do not match"})
    if response['valid']:
        return JsonResponse({'valid': response['valid'],'result': response['message'], 'authenticator':response['authenticator']})
    else:
        return JsonResponse({'valid': response['valid'],'result': response['message']})

@csrf_exempt
def login(request):
    post_data = {'username': request.POST.get("username"),
                 'password': request.POST.get("password")}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/login/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)
    if response['valid']:
        return JsonResponse({'valid': response['valid'],'result': response['message'], 'authenticator':response['authenticator']})
    else:
        return JsonResponse({'valid': response['valid'],'result': response['message']})

@csrf_exempt
def update(request, id):
    post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price")}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/update/'+str(id+'/'), data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)['message']
    return JsonResponse({'result': response})

@csrf_exempt
def delete(request, id):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/delete/' + str(id))
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)['message']
    return JsonResponse({'result': response})

@csrf_exempt
def logout(request):
    post_data = {'auth': request.POST.get("auth")}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/logout/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)
    return JsonResponse({'valid': response['valid'], 'result': response['message']})

@csrf_exempt
def auth(request):
    post_data = {'auth': request.POST.get("auth")}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/auth/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)
    return JsonResponse({'valid': response['valid'], 'result': response['message']})