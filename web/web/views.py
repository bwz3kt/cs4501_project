from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .forms import *
import json
import urllib.request
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

def login_required(f):
    def wrap(request, *args, **kwargs):
        if (request.COOKIES.get('auth') is None):
            authenticated = False
        else:
            post_data = {'auth': request.COOKIES.get('auth')}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/auth/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            print(resp['valid'])
            if resp['valid'] == True:
                authenticated = True
            else:
                authenticated = False
        # authentication failed
        if not authenticated:
            # redirect the user to the login page
            return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)
    return wrap

@login_required
@csrf_exempt
def index(request):
    req = urllib.request.Request('http://exp-api:8000/v1/home')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})

@login_required
@csrf_exempt
def top(request):
    req = urllib.request.Request('http://exp-api:8000/v1/top')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})

@login_required
@csrf_exempt
def price(request):
    req = urllib.request.Request('http://exp-api:8000/v1/price')
    response = urllib.request.urlopen(req).read().decode('utf-8')
    json_req = json.loads(response)
    context = {"json_req": json_req}
    return render(request, "foo/home.html", {"objects":json_req['results']})

@login_required
@csrf_exempt
def intro(request):
    return render(request, "foo/intro.html")

@login_required
@csrf_exempt
def create(request):
    if request.method == "GET":
        form = CreateForm()
        return render(request, "myapp/create.html", {'form': form, 'message': ""})
    else:
        form = CreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': request.POST.get("name"), 'price': request.POST.get("price"), 'auth': request.COOKIES.get('auth')}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/create/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        #     resp = json.loads(resp_json)
        #     print(resp)
        # #If valid is false, this means we have a duplicate name being entered.
        #     if resp['result'] == ('Apartment name already exists.  No duplicate entries are allowed.'):
        #     #    return render(request, "myapp/create.html", {'form': form, 'message': 'Cannot create apartment.  Apartment name already exists.'})
        #         #return JsonResponse(resp)
        #         empty_form = LoginForm()
        #         return render(request, "myapp/create.html", {'form': empty_form, 'message': resp['result']})
        #     #return redirect('/')
        #     else:
            return redirect('/home')

@login_required
@csrf_exempt
def search(request):
    if request.method == 'GET':
        form = SearchForm()
        return render(request, "myapp/search.html", {'form': form, "message": ""})
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            post_data = {'query': form.cleaned_data['query']}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/search/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
        if resp['valid'] == False:
            return render(request, "myapp/search.html", {"form": form, 'message': resp['message']})
        else:
            empty_form = SearchForm()
            return render(request, "myapp/search.html", {"form": empty_form, "objects": resp['result']})
            #return render(request, "myapp/search_results.html", {"objects": resp['result']})

@csrf_exempt
def signup(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "registration/signup.html", {'form': form, 'message': ""})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            post_data = {'username': request.POST.get("username"), 'email': request.POST.get("email"), 'password': request.POST.get("password"), 'passwordConfirm': request.POST.get("passwordConfirm")}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/signup/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)



        if resp['valid'] == False:
            #return JsonResponse(resp)
            empty_form = SignupForm()
            return render(request, "registration/signup.html", {'form': empty_form, 'message': resp['result']})
            #return redirect(request, '/signup', {'form': empty_form, 'message': resp['result']})

        else:
            response = HttpResponseRedirect('/intro/')
            response.set_cookie("auth", resp['authenticator'])
            return response

@csrf_exempt
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "registration/login.html", {'form': form, 'message': ""})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {'username': request.POST.get("username"), 'password': request.POST.get("password")}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/v1/login/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
        if resp['valid'] == False:
            #return JsonResponse(resp)
            empty_form = LoginForm()
            return render(request, "registration/login.html", {'form': empty_form, 'message': resp['result']})
            #return redirect('/')
        else:
            response = HttpResponseRedirect('/intro/')
            response.set_cookie("auth", resp['authenticator'])
            return response

@login_required
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
        return redirect('/home')

@login_required
@csrf_exempt
def details(request, id):
    req = urllib.request.Request('http://exp-api:8000/v1/get_details/' + str(id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp['valid'] == True:
        return render(request, 'myapp/view.html', {'apartment': resp['result'][0]})
    else:
        #return JsonResponse(resp)
        return redirect('/home')
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

@login_required
@csrf_exempt
def delete(request, id):
    req = urllib.request.Request('http://exp-api:8000/v1/delete/' + str(id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return redirect('/home')

@login_required
@csrf_exempt
def logout(request):
    # if (request.COOKIES.get('auth') is not None or ''):
    post_data = {'auth': request.COOKIES.get('auth')}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/v1/logout/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp['valid'] == False:

        return redirect('/home')
        #return JsonResponse(resp)
    else:
        response = HttpResponseRedirect('/')
        response.delete_cookie("auth")
        return response
    # else:
    #     return  JsonResponse({'valid': False, 'message': ""})
