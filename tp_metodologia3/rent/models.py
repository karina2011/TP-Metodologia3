from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=45)
    province = models.CharField(max_length=45)

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    capacity = models.IntegerField()
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, null=False, on_delete=models.SET('null'))
    image = models.ImageField(upload_to='rent/img/', null=True)

    class Meta:
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateTimeField()
    total = models.IntegerField()
    reservationCode = models.IntegerField()
    property = models.ForeignKey(Property, null=False, on_delete=models.SET('null'), default=1) #property es una palabra reservada y por eso sale en verde
    user = models.ForeignKey(User, null=True, on_delete=models.SET('null'), blank=True)

    class Meta:
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return datetime.strftime(self.date, '%d/%m/%Y')


class RentDate(models.Model):
    date = models.DateTimeField()
    property = models.ForeignKey(Property, null=False, on_delete=models.SET('null'), default=1)
    reservation = models.ForeignKey(Reservation, null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        verbose_name_plural = 'Fechas de Alquileres'

    def __str__(self):
        return self.date.__format__("%Y-%m-%d %H:%M:%S")
