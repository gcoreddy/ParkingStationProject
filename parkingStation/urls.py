from parking.views import parkingRestAPI, getQuery
from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()

prestApi = parkingRestAPI()

urlpatterns = [
    url('^$', getQuery, name='getQuery'),
    url(r'^admin/',admin.site.urls),
    url(r'^add$', prestApi.addCar, name='addCar'),
    url(r'^remove$', prestApi.removeCar, name='removeCar'),
    url(r'^list$', prestApi.displayCars, name='displayCars'),
]