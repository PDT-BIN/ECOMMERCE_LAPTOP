from django.contrib import admin
from . import models


admin.site.register(models.State)
admin.site.register(models.DeliveryAddress)
admin.site.register(models.Order)
admin.site.register(models.OrderDetails)
admin.site.register(models.ReturnForm)
admin.site.register(models.ReturnDetails)
