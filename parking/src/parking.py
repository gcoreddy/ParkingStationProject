import time
import sys
import json
import django
from parking.models import TariffPlan, carDataDetails, ParkingLevel 
from parking.src.Ticket import Ticket
from parking.src.common import parkingExceptionsDict, LevelWithTheSameName, ParkingLevelDoesntExist, NoSpaceLeftInParking, CarWithSameNumExist

class ParkingStation:
    '''Class for Parking station to add or remove cars,
	   also for extending the Levels, updating tariff plans'''
    def __init__(self):
        '''Constructor method'''
        self.jsonDec = json.decoder.JSONDecoder()
	
    def __displayLevels(self):
        ''' Returns the existing parking levels in the parking station.'''
        levelInfoDict = {"LevelInfo" : []}

        # Retrieve the parking level details from each and every level.
        for level in ParkingLevel.objects.all().values("level_num","free_spots","occupied_spots","total_spots"):
            levelInfoDict["LevelInfo"].append(level)
        return levelInfoDict
		
    def deleteLevel(self,level_name):
        ''' Delete or close a specific parking level from the station.'''
        ParkingLevel.objects.filter(level_num=level_name).delete()
        
    def addLevel(self,level_name,total_spots):
        '''Add or extend a new parking llevel to the station.'''
        if len(ParkingLevel.objects.filter(level_num=level_name)) > 0:
            # Check whether a parking level with the same name already exist.
            return parkingExceptionsDict["LevelWithTheSameName"]

        # Update the free spots and occupied spots based on total spots.
        free_spots  = list(range(1,int(total_spots)+1))
        occupied_spots = []
        
        # Create a new level with the details provided.
        level = ParkingLevel(level_num=level_name,total_spots=total_spots,free_spots=json.dumps(list(free_spots)),occupied_spots=json.dumps(list(occupied_spots)))
        level.save()
        return self.__displayLevels()

    def __getAvailableLocation(self):
        '''Retrieves and returns an available spot by searching from all the available Levels.'''
        location = None
        if len(ParkingLevel.objects.all()) == 0:
            # Check whether atleast one parking level exist.
            raise ParkingLevelDoesntExist
        for level in ParkingLevel.objects.all():
            # Searching for free spots in each parking level.
            free_spots = list(self.jsonDec.decode(level.free_spots))
            if len(free_spots) > 0:
                # Assign a parking spot in this specific level if free spots available.
                assignedSpot = free_spots[-1]
                location = level.level_num + "_" + str(assignedSpot)
                break
        # Raise an exception if no space left in any of the parking level.
        if location is None: raise NoSpaceLeftInParking
        return location
        
    def __checkCarNo(self,car_num):
        '''Check whether car with the name exist in the parking slot.'''
        try:
            # Retrieving the car details with the name.
            car = carDataDetails.objects.get(carno=car_num)
        except carDataDetails.DoesNotExist:
            # Do nothing and try to assign a spot for the car 
            # if car number not exist in the parking.
            pass
        else:
            # Raise an exception if car already there with the same name.
            raise CarWithSameNumExist

    def addCar(self, car_num, plan_name):
        '''Add/Allocate a available spot to a car in the parking.'''
        try:
            tariff = TariffPlan.objects.get(plan=plan_name)
            inTime=time.time()
            # Get the available free spot.
            location = self.__getAvailableLocation()
            # Check the car existance in the parking.
            self.__checkCarNo(car_num)
            # Create a new car object in the database.
            newCar = carDataDetails.objects.create(carno=car_num,tariff_plan=plan_name,inTime=inTime,location=location)
            newCar.save()
            # Assign a spot to the car.
            self.__assignSpot(location)
            # Create Ticket with fare details.
            ticket = Ticket(location)
            receipt = ticket.printTicket("Entry")
        except ParkingLevelDoesntExist:
            # Exception if no parking level exist.
            receipt = parkingExceptionsDict["ParkingLevelDoesntExist"]
        except NoSpaceLeftInParking:
            # Exception if no free spots available in the parking.
            receipt = parkingExceptionsDict["NoSpaceLeftInParking"]
        except CarWithSameNumExist:
            # Exception if there is car with the same name in parking.
            receipt = parkingExceptionsDict["CarWithSameNumExist"]
        except TariffPlan.DoesNotExist:
            # Exception if there is no tariff plan defined.
            receipt = parkingExceptionsDict["TariffPlanDoesntExist"]
        finally:
            return receipt
            
    def removeCar(self, location):
        ''' This method removes a car based on specific location 
		    from the parking space and make it available for next cars. 
		'''
        try:
            # Create Ticket with fare details.
            ticket = Ticket(location)
            receipt = ticket.printTicket("Exit")
            # Delete the car object from database.
            carDataDetails.objects.get(location=location).delete()
            # Unassign or free the occipied spot of the car.
            self.__unAssignSpot(location)
        except TariffPlan.DoesNotExist:
            # Exception if tariffplan doesn't exist.
            receipt = parkingExceptionsDict["TariffPlanDoesntExist"]
        except carDataDetails.DoesNotExist:
            # Exception if the spcified location if already free.
            receipt = parkingExceptionsDict["LocationEmpty"]
        except carDataDetails.MultipleObjectsReturned:
            # Exception if there is multiple cars allocated with the same location.
            receipt = parkingExceptionsDict["MultipleCarsWithSameLocation"]
        finally:
            return receipt
		
    def displayCars(self):
        ''' This method diplays all the cars that are parked. '''
        carDetailsDict = {"cars": []}
        for car in carDataDetails.objects.values("carno", "tariff_plan", "location", "inTime"):
            # Retrieve and return each car details parked in the parking station.
            car["inTime"] = time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(car["inTime"])))
            carDetailsDict["cars"].append(car)
        carDetailsDict['code'] = 204 if len(carDetailsDict['cars']) == 0 else 200
        return carDetailsDict
		
    def __assignSpot(self,location):
        '''This method assigns an available spot to the car 
		   in the specified level.
		'''
        # Retrieve level object.
        level = ParkingLevel.objects.get(level_num=location.split("_")[0])
        # Get free spots available in that level.
        free_spots = list(self.jsonDec.decode(level.free_spots))
        assignedSpot = location.split("_")[1]
        # Remove a assigned spot from free spots and update the db.
        free_spots.remove(int(assignedSpot))
        level.free_spots = json.dumps(list(free_spots))
        # Add the assigned spot in the occupied spots and update the db.
        occupiedSlots = list(self.jsonDec.decode(level.occupied_spots))
        occupiedSlots.append(assignedSpot)
        level.occupied_spots = json.dumps(list(occupiedSlots))
        level.save()
        return location

    def __unAssignSpot(self,location):
        '''This method un assigns occpied spot of the car at exit.'''
        # Get the parking object.
        level = ParkingLevel.objects.get(level_num=location.split("_")[0])
        # Un assign the spot from occupied spot and add it in the free spots.
        assignedSpot = location.split("_")[1]
        free_spots = list(self.jsonDec.decode(level.free_spots))
        free_spots.append(int(assignedSpot))
        level.free_spots = json.dumps(list(free_spots))
        occupiedSlots = list(self.jsonDec.decode(level.occupied_spots))
        occupiedSlots.remove(assignedSpot)
        level.occupied_spots = json.dumps(list(occupiedSlots))
        level.save()
