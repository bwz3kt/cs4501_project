from django.http import JsonResponse
import json
import urllib.request
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import hashers
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import *
from kafka import KafkaProducer
import copy
from elasticsearch import Elasticsearch


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
    response = json.loads(response)
    if response['valid'] == True:
        return JsonResponse({'valid': response['valid'], 'result': response['result']})
    else:
        return JsonResponse(response)

@csrf_exempt
def profile(request, username):
    template_data = urllib.request.Request('http://models-api:8000/api/v1/profile/' + str(username))
    response = urllib.request.urlopen(template_data).read().decode('utf-8')
    response = json.loads(response)
    # if response['valid'] == True:
    #     return JsonResponse({'valid': response['valid'], 'result': response['result'], 'user': response['user']})
    # else:
    return JsonResponse(response)

@csrf_exempt
def user_profile(request):
    post_data = {'auth': request.POST.get('auth')}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/user_profile/', data=post_encoded, method='POST')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(response)
    # if response['valid'] == True:
    #     return JsonResponse({'valid': response['valid'], 'result': response['result'], 'user': response['user']})
    # else:
    return JsonResponse(response)

@csrf_exempt
def create(request):
    post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price"), 'auth': request.POST.get('auth')}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/create/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = json.loads(resp_json)
    if response['valid'] == True:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        new_listing = response['result']
        producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))
    return JsonResponse({'result': response['message']})

@csrf_exempt
def search(request):
    query = request.POST.get('query')
    es = Elasticsearch(['es'])
    objs = []
    post_copy = copy.copy(request.POST)
    del post_copy['query']
    del post_copy['user']
    filters=[]
    keys=[]
    values=[]
    for key, value in post_copy.items():
        print(post_copy[key])
        print(key)
        values.append(post_copy[key])
        keys.append(key)
        if post_copy[key] == 'True':
            filters.append(key)
    print(filters)
    if request.POST.get('user') == 'True':
        result = es.search(index='user_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
    # else:
        # if "id" in filters:
        #     result = es.search(index='listing_index', body={'query':{'query_string': {"fields":filters,'query': query}},'size':10})
    #if name filter is checked and the query is not a number, only search for the apartments with name matching the query since there is a data type issue otherwise
    elif request.POST.get('name') == 'True' and not request.POST.get('query').isdigit():
        result = es.search(index='listing_index', body={'query': {'query_string': {"fields": ['name'], 'query': query}}, 'size': 10})
    else:
        #If name filter is not checked and there exist filters and the query is not a number, then return false since there is a data type issue
        if request.POST.get('name') == 'False' and len(filters) != 0 and not request.POST.get('query').isdigit():
            response = {'valid': False,
                        'message': 'Error.  Data type conflict.  Query is a string but id and price filters only accept numbers.'}
            return JsonResponse(response)
        #else, just use the filters normally and make sure that for the filters that are checked, they match the query
        result = es.search(index='listing_index', body={'query': {'query_string': {"fields":filters,'query': query}},'size': 10})
    if result['timed_out'] == True:
        response = {'valid': False, 'message': 'Search timed out'}
        return JsonResponse(response)

    for element in result['hits']['hits']:
        objs.append(element['_source'])

    if request.POST.get('user') == 'True':
        objs.sort(key=lambda x: x['username'])
    else:
        objs.sort(key=lambda x: x['id'])
    response = {'valid': True, 'result': objs, 'user': request.POST.get('user')}
    return JsonResponse(response)

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
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        new_listing = response['result']
        producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))

        return JsonResponse({'valid': response['valid'],'result': response['message'], 'authenticator':response['authenticator'], 'obj': response['result']})
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