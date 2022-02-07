from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    Name = models.CharField(
        null=False,
        max_length=20,
        )
    Description = models.CharField(
        null=False,
        max_length=20,
        )
    Slogan = models.CharField(
        null=False,
        max_length=20,
        )

    def __str__(self):
        return "CarMake: " + self.Name  + \
                " - Descritpion: " + self.Description + \
                "\nSlogan: " + self.Slogan


# <HINT> Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    NOT_SPEC = ' '
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    SPORT = 'Sport'
    CAR_TYPES = [
        (NOT_SPEC,'N/A'),
        (SEDAN,'Sedan'),
        (SUV,'SUV'),
        (WAGON,'WAGON'),
        (SPORT,'Sport')
        ]
    CarMake = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
        )
    DealerId = models.IntegerField(
        default=-1
        )
    Name = models.CharField(
        null=False,
        max_length=20,
        )
    Type = models.CharField(
        max_length=7,
        choices=CAR_TYPES,
        default=NOT_SPEC
        )
    Year = models.DateField(
        null=False
        )

    def __str__(self):
        return "Car Model: " + self.Name + \
                ", Type: " + self.Type + \
                ", Year: " + str(self.Year) + \
                ", DealerId: " + str(self.DealerId) + \
                ", Car Make: <" + str(self.CarMake) + " >"


# class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, state, st, zip):
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
        self.state = state
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name + \
                ", City: " + self.city + \
                ", State: " + self.state + \
                ", st: " + self.st


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealer_id, id, name, purchase, review, make, model, year, purchase_date):
        self.make = make
        self.model = model
        self.year = year
        self.dealer_id = dealer_id
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = ""

    def __str__(self):
        return "Customer Name: " + self.name

