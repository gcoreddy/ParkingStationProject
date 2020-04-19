from django.shortcuts import render
from parking.src.Ticket import Ticket
from parking.src.common import CustomException
from parking.src.parking import ParkingStation
from django.http import JsonResponse


class parkingRestAPI():
    def __init__(self):
        self.pstation = ParkingStation()

    # For rest api invocation.
    def addCar(self, request):
        '''Adds a car to the parking lot.'''
        car_num = request.GET.get('car_num')
        tariff_plan = request.GET.get('tariff_plan')
        if car_num is None:
            # Throws CustomException when car num is not provided in input.
            return JsonResponse(CustomException("NoCarNumProvided").value)
        elif tariff_plan is None:
            # Throws CustomException when tariff is not provided in input.
            return JsonResponse(CustomException("NoTariffPlanProvided").value)
        else:
            return JsonResponse(self.pstation.addCar(car_num, tariff_plan),
                                safe=False)

    def removeCar(self, request):
        '''Removes a car from a prking lot.'''
        location = request.GET.get('location')
        if location is None:
            # Throws CustomException when location is not provided in input.
            return JsonResponse(CustomException("NoLocationProvided").value)
        else:
            # Removes a car and un assignes the parking lot.
            return JsonResponse(self.pstation.removeCar(location),safe=False)

    def displayCars(self, request):
        '''Returns a dictionary with cars parked.'''
        return JsonResponse(self.pstation.displayCars(),safe=False)

# For Web api invocation.
def getQuery(request):
    pstation = ParkingStation()
    if request.method == 'GET':
        return render(request, 'index.html', {})
    elif request.method == 'POST':
        if request.POST['OPTION'] == "create_tariff_plan":
            output = Ticket.create_tariff(request.POST['plan'],request.POST['cost'],request.POST['freetime'])
            return JsonResponse(dict(output), safe=False)
        elif request.POST['OPTION'] == "update_tariff_plan":
            output = Ticket.update_tariff(request.POST['plan_name'],
                                          request.POST['plan_cost'],
                                          request.POST['plan_freetime']
                                         )
            return JsonResponse(output, safe=False)
        elif request.POST['OPTION'] == "add_car":
            return JsonResponse(pstation.addCar(request.POST['car_num'],
                                                request.POST['tariff_plan']
                                               ),
                                safe=False)
        elif request.POST['OPTION'] == "remove_car":
            return JsonResponse(pstation.removeCar(request.POST['location']),
                                safe=False)
        elif request.POST['OPTION'] == "display_car":
            return JsonResponse(pstation.displayCars(), safe=False)
        elif request.POST['OPTION'] == "add_level":
            return JsonResponse(pstation.addLevel(
                                                  request.POST['level_name'],
                                                  request.POST['parking_spots']
                                                 ),
                                safe=False)
    else:
        print(request.POST['OPTION'])
