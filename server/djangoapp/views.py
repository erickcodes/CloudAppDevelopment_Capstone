from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import DealerReview, CarDealer, CarModel
# from .restapis import related methods
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# API URLS and keys
review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/40c37a61-b3dc-4acf-9a9b-ca73fc48e1ef/dealership-package/review"
dealership_url = "https://us-south.functions.appdomain.cloud/api/v1/web/40c37a61-b3dc-4acf-9a9b-ca73fc48e1ef/dealership-package/dealership"

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
            return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to index
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(dealership_url)
        context = dict()
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        # Concat all dealer's short name
        # reviews_desc = ' '.join([review.review for review in reviews])
        context = dict()
        context['review_list'] = reviews
        context['dealer_id'] = dealer_id
        context['dealer_name'] = [dealer.full_name for dealer in get_dealers_from_cf(dealership_url)][0]
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = dict()
        context['dealer_id'] = dealer_id
        context['dealer_name'] = [dealer.full_name for dealer in get_dealers_from_cf(dealership_url)][0]
        context['cars'] = CarModel.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        if request.user.is_authenticated:
            review = dict()
            print(request.POST)
            review["id"] = len(get_dealer_reviews_from_cf(review_url, dealer_id)) + 1 # lazy count
            review["name"] = request.POST['name']
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            if request.POST.get('purchasecheck', 'false') == 'True':   
                car = CarModel.objects.get(pk=int(request.POST['car']))
                review["car_make"] = car.car_make.name
                review["car_model"] = car.model
                review["car_year"] = car.year.year
                review["purchase"] = bool(request.POST['purchasecheck'])
                review["purchase_date"] = request.POST['purchasedate']
            json_payload = dict()
            json_payload["review"] = review
            post_request(review_url, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)