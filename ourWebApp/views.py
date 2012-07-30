# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.template import Template, Context

from ourWebApp.models import *

import re

@csrf_exempt
def home(request, template_name):
    password_error = ""
    user = None
    
    if 'username' in request.POST:
        username = User.objects.filter(username=request.POST['username'])
        if username:
            username = username[0]
            user = auth.authenticate(username=username, password=request.POST['user_password'])
    
    if user and user.is_active:
        auth.login(request, user)
        request.session["currentUser"] = username
        return HttpResponseRedirect("/profile/%s" % username )
    else:
        return render_to_response(template_name, {})

@csrf_exempt
def signUp(request, template_name):
    username = ""
    email_address = ""
    user_password = ""
    name_error = ""
    email_error = ""
    password_error = ""
    password_confirm_error = ""
    user_password_confirm = ""
    
    if 'user_password' in request.POST:
        password_error = "OK"
        user_password = request.POST['user_password']
        if 'user_password_confirm' in request.POST:
            user_password_confirm = request.POST['user_password_confirm']
            if user_password != user_password_confirm:
                password_confirm_error = "Passwords do not match"
            else:
                password_confirm_error = "OK"
    if 'username' in request.POST:
        username = request.POST['username']
        name_error = "OK"
    if 'email_address' in request.POST:
        email_address = request.POST['email_address']
        if not isEmail(email_address):
            email_error = "Invalid email address"
        else:
            email_error = "OK"
    if name_error == "OK" and email_error == "OK" and password_error == "OK" and password_confirm_error == "OK":
		new_user = User.objects.create_user(username, email_address, user_password)
		new_user.save()
		dealer = Dealer(user=new_user,dealer_name=request.POST['business_name'])
		dealer.save()
		request.session['currentUser'] = username
		return HttpResponseRedirect("/profile/%s" % username)
    else:
        return render_to_response(template_name, 
        {'name_error':name_error, 'email_error':email_error, 'password_error':password_error, 'password_confirm_error':password_confirm_error,
        'username':username, 'email_address':email_address, 'user_password':user_password, 'user_password_confirm':user_password_confirm
        })

def profile(request, user, template_name):
    if 'search_query' in request.GET:
        return HttpResponseRedirect("http://localhost:8000/search/?search_query=%s" % request.GET['search_query'])
    else:
        current_user=User.objects.filter(username=user)
        if current_user:
            current_user = current_user[0]
            dealer_name = Dealer.objects.filter(user=current_user)
            if dealer_name:
                dealer_name = dealer_name[0]
            else:
                return HttpResponseRedirect("/")
            return render_to_response(template_name, {'dealer_name':dealer_name})   
        else:
            return HttpResponseRedirect("")

def myprofile(request, template_name):
    if 'search_query' in request.GET:
        return HttpResponseRedirect("/search/?search_query=%s" % request.GET['search_query'])
    else:
        current_user=User.objects.filter(username=request.session['currentUser'])
        if current_user:
            current_user = current_user[0]
            dealer_name = Dealer.objects.filter(user=current_user)
            if dealer_name:
                dealer_name = dealer_name[0]
            else:
                return HttpResponseRedirect("/")
            return render_to_response(template_name, {'dealer_name':dealer_name})   
        else:
            return HttpResponseRedirect("")

def mytransactions(request, template_name):
	if 'search_query' in request.GET:
		return HttpResponseRedirect("http://localhost:8000/search/?search_query=%s" % request.GET['search_query'])
	else:
		t = get_template(template_name)
		currentDealer = getDealerName(request)
		c = Context({'dealer_name':currentDealer})
	return HttpResponse(t.render(c))
	
def search(request, template_name):
    matches = None
    if 'search_query' in request.GET:
        query = request.GET['search_query']
        matches = Item.objects.filter(item_name__contains=query)
    else:
        print 'no query'
    return render_to_response(template_name, {'query_matches':matches})

@csrf_exempt
def mystore(request, template_name):
    addItemButtonPressed = False
    if 'search_query' in request.GET:
        return HttpResponseRedirect("http://localhost:8000/search/?search_query=%s" % request.GET['search_query'])
    print request.session['currentUser']
    dealer = Dealer.objects.get(user=User.objects.get(username=request.session['currentUser']))
    items_sold = Item.objects.filter(dealer=dealer)
    if 'add_item' in request.POST:
        addItemButtonPressed = True
    elif 'add_item_toDB' in request.POST:
        product = {}
        product['name'] = request.POST['product_name']
        product['price'] = request.POST['product_price']
        if isValidProduct(product):
            add_item_to_database( request, request.POST['product_name'], request.POST['product_price'] )
    return render_to_response(template_name, {'dealer_name':dealer.dealer_name, 'items_sold':items_sold, 'add_pressed':addItemButtonPressed})
    
def add_item_to_database( request, product_name, product_price):
    user = User.objects.get(username=request.session['currentUser'])
    dealer = Dealer.objects.get(user=user)
    i = Item(item_name=product_name, item_price=float(product_price), dealer=dealer)
    i.save()
    
def isValidProduct(product):
    name_pattern = re.compile("(\w)+")
    price_pattern = re.compile("\d[\d\,\.]*")
    if name_pattern.match(product['name']) and price_pattern.match(product['price']):
        return True
    else:
        return False

@csrf_exempt		
def mycarts(request, template_name):
	if 'search_query' in request.GET:
		return HttpResponseRedirect("http://localhost:8000/search/?search_query=%s" % request.GET['search_query'])
	else:
		carts = Cart.objects.filter(owner=Dealer.objects.get(user=User.objects.get(username=request.session['currentUser'])))
		t = get_template(template_name)
		if 'add_cart' in request.POST:
			c = Context({'carts':carts, 'addCartEnabled':True})
		else:
			c = Context({'carts': carts, 'addCartEnabled':False})
		if 'create_cart' in request.POST:
			addCartToDB(request)
		return HttpResponse(t.render(c))

def addCartToDB(request):
	cart = Cart(name=request.POST['cart_name'], owner=Dealer.objects.get(user=User.objects.get(username=request.session['currentUser'])))
	cart.save()
	
def removeitem(request, item_id, template_name):
	item = Item.objects.get(id=item_id)
	owner = item.dealer.user.username
	user = request.session['currentUser']
	print owner
	print user
	if str(user) == owner:
		item.delete()
	else:
		print "not the same user"
	return HttpResponseRedirect("/my_store/")
		
        
def getDealerName(request):
	dealer = Dealer.objects.get(user=User.objects.get(username=request.session['currentUser']))
	return dealer.dealer_name
	
def logout(request):
    if 'currentUser' in request.session:
        del request.session['currentUser']
    return HttpResponseRedirect("/")

def isEmail(input):
    pattern = re.compile("(\w+@[a-zA-Z_]+(\.[a-zA-Z]{2,4})+)")
    if pattern.match(input):
        return True
    else:
        return False

