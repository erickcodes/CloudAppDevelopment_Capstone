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
class CarDealer(models.Model):
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=20)
    st = models.CharField(max_length=2)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    lat_cord = models.FloatField()
    long_cord = models.FloatField()
    short_name = models.CharField(max_length=25)
    full_name = models.CharField(max_length=75)

    def __str__(self):
        return full_name + ", address: " + self.address + ", " + self.city + ", " + self.st

# <HINT> Create a plain Python class `DealerReview` to hold review data
