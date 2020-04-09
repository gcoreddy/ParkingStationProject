from django.contrib import admin
from parking import models as m

admin.site.register(m.TariffPlan)
admin.site.register(m.carDataDetails)
admin.site.register(m.ParkingLevel)