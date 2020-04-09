from django.shortcuts import render
from parking.src.Ticket import Ticket
from parking.src.parking import ParkingStation
from django.http import JsonResponse


class parkingRestAPI():
    def __init__(self):
        self.pstation = ParkingStation()

    # For rest api invocation.
    def addCar(self,request):
        try:
            car_num = request.GET['car_num']
            tariff_plan = request.GET['tariff_plan']
        except:
            responseDict = {"status" : "error", "code" : 400, "Reason": "<car_num> and <tariff_plan> should be provided."}
        else:
            responseDict = self.pstation.addCar(car_num,tariff_plan)
        return JsonResponse(responseDict,status=responseDict['code'],safe=False)

    def removeCar(self,request):
        try:
            location = request.GET['location']
        except:
            responseDict = {"status" : "error", "code": 400, "Reason": "<location> should be provided as input."}
        else:
            responseDict = self.pstation.removeCar(location)
        return JsonResponse(responseDict,status=responseDict['code'],safe=False)

    def displayCars(self,request):
        responseDict = self.pstation.displayCars()
        return JsonResponse(self.pstation.displayCars(),status=responseDict['code'],safe=False)

# For Web api invocation.
def getQuery(request):
    pstation = ParkingStation()
    if request.method == 'GET':
        return render(request, 'index.html', {})
    elif request.method == 'POST':
        if request.POST['OPTION'] == "1":
            output = Ticket.createOrUpdateTariff(request.POST['plan'],request.POST['cost'],request.POST['freetime'])
            return JsonResponse(output,safe=False)
        elif request.POST['OPTION'] == "2":
            return JsonResponse(pstation.addCar(request.POST['car_num'],request.POST['tariff_plan']),safe=False)
        elif request.POST['OPTION'] == "3":
            return JsonResponse(pstation.removeCar(request.POST['location']),safe=False)
        elif request.POST['OPTION'] == "4":
            return JsonResponse(pstation.displayCars(),safe=False)
        elif request.POST['OPTION'] == "5":
            return JsonResponse(pstation.addLevel(request.POST['level_name'],request.POST['parking_spots']),safe=False)
    else:
        print(request.POST['OPTION'])
