from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.name


class Owner_Ship(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    capacity = models.IntegerField()
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, null=False, on_delete=models.SET('null'))
    image = models.ImageField(upload_to='application/img', null=True)

    class Meta:
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return self.description


class Reservation(models.Model):
    date = models.DateTimeField()
    code = models.IntegerField()
    total = models.IntegerField()
    owner_ship = models.ForeignKey(Owner_Ship, null=False, on_delete=models.SET('null'))

    class Meta:
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return datetime.strftime(self.date, '%d/%m/%Y')


class Rent_Date(models.Model):
    date = models.DateTimeField()
    owner_ship = models.ForeignKey(Owner_Ship, null=False, on_delete=models.SET('null'))
    reservation = models.ForeignKey(Reservation, null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        verbose_name_plural = 'Fechas de Alquileres'

    def __str__(self):
        return self.date.__format__("%Y-%m-%d %H:%M:%S")
