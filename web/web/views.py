from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .forms import *
import json
import urllib.request
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    req = urllib.request.Request('http://exp-api:8000/v1/home')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})


@csrf_exempt
def top(request):
    req = urllib.request.Request('http://exp-api:8000/v1/top')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})

@csrf_exempt
def price(request):
    req = urllib.request.Request('http://exp-api:8000/v1/price')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})

@csrf_exempt
def intro(request):
    return render(request, "foo/intro.html")

@csrf_exempt
def create(request):
    if request.method == "GET":
        form = CreateForm()
        return render(request, "myapp/create.html", {'form': form})
    else:
        form = CreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price")}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/create/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            # resp = json.loads(resp_json)
        return redirect('/')

@csrf_exempt
def signup(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "registration/signup.html", {'form': form})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            post_data = {'username': request.POST.get("username"), 'email': request.POST.get("email"), 'password': request.POST.get("password"), 'passwordConfirm': request.POST.get("passwordConfirm")}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/signup/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
        if resp['valid'] == False:
            return JsonResponse(resp)
        return redirect('/')

@csrf_exempt
def update(request, id):
    if request.method == "GET":
        form = UpdateForm()
        return render(request, "myapp/create.html", {'form': form})
    else:
        form = UpdateForm(request.POST)
        if form.is_valid():
            post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price")}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/update/'+str(id)+'/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            # resp = json.loads(resp_json)
        return redirect('/')

@csrf_exempt
def details(request, id):
    req = urllib.request.Request('http://exp-api:8000/v1/get_details/' + str(id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'myapp/view.html', {'apartment': resp['result'][0]})
    # if request.method == "GET":
    #     form = CommentForm()
    #     return render(request, 'myapp/view.html', {'apartment': resp['result'][0])
    # else:
    #     form = CommentForm(request.POST)
    #     # post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price")}
    #     # post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    #     # req = urllib.request.Request('http://exp-api:8000/v1/create/', data=post_encoded, method='POST')
    #     # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #     # resp = json.loads(resp_json)
    # return redirect('/')

@csrf_exempt
def delete(request, id):
    req = urllib.request.Request('http://exp-api:8000/v1/delete/' + str(id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return redirect('/')
