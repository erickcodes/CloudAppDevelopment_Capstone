from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    # - Any other fields you would like to include in car make model

    def __str__(self):
        return "Make: " + self.name + ", Description: " + self.description



class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake ,on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=20)
    year = models.DateField()
       # - Any other fields you would like to include in car model

    def __str__(self):
        return "Model: " + self.model + ", Type: " + self.car_type 


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Buyer's dealership
        self.dealership = dealership
        # Buyer's name
        self.name = name
        # Buyer's purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Buyer's purchase_date
        self.purchase_date = purchase_date
        # Buyer's car_make
        self.car_make = car_make
        # Buyer's car_model
        self.car_model = car_model
        # Buyer's car_year
        self.car_year = car_year
        # Buyer's sentiment
        self.sentiment = sentiment
        # Review ID
        self.id = id

    def __str__(self):
        return "Reviewer's name: " + self.name
