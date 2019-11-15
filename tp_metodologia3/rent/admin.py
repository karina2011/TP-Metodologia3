from django.contrib import admin

# Register your models here.
from rent.models import City, Property, Reservation, RentDate


class RentDate_Inline(admin.TabularInline):
    model = RentDate
    fk_name = "property"
    max_num = 7


class OwnerShipAdmin(admin.ModelAdmin):
    inlines = [RentDate_Inline, ]


admin.site.register(City)
admin.site.register(RentDate)
admin.site.register(Reservation)
admin.site.register(Property, OwnerShipAdmin)

