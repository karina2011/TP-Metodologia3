from django.contrib import admin

# Register your models here.
from rent.models import City, Owner_Ship, Reservation, Rent_Date


class Date_Rent_Inline(admin.TabularInline):
    model = Rent_Date
    fk_name = "owner_ship"
    max_num = 7


class OwnerShipAdmin(admin.ModelAdmin):
    inlines = [Date_Rent_Inline, ]


admin.site.register(City)
admin.site.register(Rent_Date)
admin.site.register(Reservation)
admin.site.register(Owner_Ship, OwnerShipAdmin)

