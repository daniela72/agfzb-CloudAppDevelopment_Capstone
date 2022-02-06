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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
