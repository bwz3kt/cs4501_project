from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rating = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        max_digits=3,
        decimal_places=2
    )

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    rating = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    associated_apt = models.ForeignKey('Apartment')

