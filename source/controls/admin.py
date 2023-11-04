from django.contrib import admin
from . import models


admin.site.register(models.Category)
admin.site.register(models.Specification)
admin.site.register(models.Manufacturer)
admin.site.register(models.LaptopModel)
admin.site.register(models.CartDetails)
admin.site.register(models.Supplier)
admin.site.register(models.ReservationForm)
admin.site.register(models.ReservationDetails)
admin.site.register(models.ImportationForm)
admin.site.register(models.ImportationDetails)
admin.site.register(models.LiquidationForm)
admin.site.register(models.Laptop)
