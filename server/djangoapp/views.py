from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from .models import CarModel
# from .models import related models
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        # remove courses/ and works
        # link displays registration only. Not user_registration_bootstrap.html
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password1 = request.POST['psw1']
        password2 = request.POST['psw2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        # check match password
        if not password1 == password2:
            context['message'] = "Passwords do not match."
            return render(request, 'djangoapp/registration.html', context)
        user_exist = False
        try:
            # check if user exists
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password1)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://2fe3d546.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        # Get reviews from the URL
        url = "https://2fe3d546.us-south.apigw.appdomain.cloud/api/review"        
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        #reviews_all = ' '.join([review.review for review in reviews_list])
        context["reviews_list"] = reviews
        urlSearch = "https://2fe3d546.us-south.apigw.appdomain.cloud/api/search"        
        dealer_by_id = get_dealer_by_id(urlSearch, dealerId)
        context["dealer_info"] = dealer_by_id[0]
        context["dealerId"] = dealerId
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details_search(request, dealerId):
    context = {}
    if request.method == "GET":
        # Get reviews from the URL
        url = "https://2fe3d546.us-south.apigw.appdomain.cloud/api/search"        
        dealer_by_id = get_dealer_by_id(url, dealerId)
        #reviews_all = ' '.join([review.review for review in reviews_list])
        context["dealer_info"] = dealer_by_id
        context["dealerId"] = dealerId
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    user = request.user 
    if user.is_authenticated:
        cars = CarModel.objects.filter(DealerId=dealer_id)
        context['cars'] = cars
        context["dealer_id"] = dealer_id
        if request.method == "GET":
            if len(cars) == 0:
                messages.add_message(request, messages.WARNING, \
                        'This Dealer does not sell cars yet.')
            urlSearch = "https://2fe3d546.us-south.apigw.appdomain.cloud/api/search"        
            dealer_by_id = get_dealer_by_id(urlSearch, dealer_id)
            context["dealer_info"] = dealer_by_id[0]
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            review = {}
            review["id"] = random.randrange(100, 1000, 3)
            review["name"] = request.user.username
            review["dealership"] = int(dealer_id)
            review["review"] = request.POST['review']
            review['purchase'] = request.POST.get('purchasecheck', False)
            review["purchase_date"] = request.POST["purchasedate"]
            # get objects from selected car model
            car_model = CarModel.objects.get(id=request.POST['car'])
            review['car_make'] = car_model.CarMake.Name
            review['car_model'] = car_model.Name
            review['car_year'] = car_model.Year
            json_payload = {}
            json_payload['review'] = review
            print(f'this is the payload {json_payload}')
            url = 'https://2fe3d546.us-south.apigw.appdomain.cloud/api/review'
            json_result = post_request(url, json_payload, dealer_id=dealer_id)
            print('POST request result: ', json_result)
            try:
                if json_result['ok']:
                    # if post submission succesfull
                    messages.add_message(request, messages.SUCCESS, \
                            'Review successfully submitted')
            except:
                messages.add_message(request, messages.WARNING, json_payload)
                messages.add_message(request, messages.WARNING, json_result)
                return render(request, 'djangoapp/add_review.html', context)
            else:
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

