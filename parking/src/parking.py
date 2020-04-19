import time
import sys
import ast
import django
from parking.models import TariffPlan, carDataDetails, ParkingLevel
from parking.src.Ticket import Ticket
from parking.src.common import CustomException


class ParkingStation:
    '''Class for Parking station to add or remove cars,
       also for extending the Levels, updating tariff plans'''

    def __displayLevels(self):
        ''' Returns the existing parking levels in the parking station.'''
        levelInfoDict = {"LevelInfo": []}

        # Retrieve the parking level details from each and every level.
        for level in ParkingLevel.objects.all().values("level_num",
                                                       "free_spots",
                                                       "occupied_spots",
                                                       "total_spots"):
            levelInfoDict["LevelInfo"].append(level)
        return levelInfoDict

    def deleteLevel(self, level_name):
        ''' Delete or close a specific parking level from the station.'''
        ParkingLevel.objects.get(level_num=level_name).delete()

    def get_total_spots(self):
        totalSpots = 0
        for level in ParkingLevel.objects.all():
            totalSpots += int(level.total_spots)
        return totalSpots

    def addLevel(self, level_name, total_spots):
        '''Add or extend a new parking llevel to the station.'''
        if ParkingLevel.objects.filter(level_num=level_name).count() > 0:
            # Check whether a parking level with the same name already exist.
            return CustomException("LevelWithTheSameName").value
        # Update the free spots and occupied spots based on total spots.
        existingSpots = self.get_total_spots()
        free_spots = list(
                          range(
                                existingSpots+1,
                                int(total_spots)+1+existingSpots)
                         )
        occupied_spots = []

        # Create a new level with the details provided.
        try:
            level = ParkingLevel(level_num=level_name, total_spots=total_spots,
                                 free_spots=str(free_spots),
                                 occupied_spots=str(occupied_spots))
            level.save()
        except:
            return CustomException("FailedCreateParkingLevel").value
        else:
            return self.__displayLevels()

    def addCar(self, car_num, plan_name):
        '''Add/Allocate an available spot to a car in the parking.'''
        try:
            if TariffPlan.objects.filter(tariff_plan=plan_name).count() == 0:
                raise CustomException("TariffPlanDoesntExist")
            inTime = time.time()
            # Check the car existance in the parking.
            if carDataDetails.objects.filter(carno=car_num).count() == 0:
                # Create a new car object in the database.
                tariff_plan = TariffPlan.objects.get(tariff_plan=plan_name)
                # Assign a available spot to the car.
                location = self.__assignSpot()
                newCar = carDataDetails.objects.create(carno=car_num,
                                                       tariff_plan=tariff_plan,
                                                       inTime=inTime,
                                                       location=location)
                newCar.save()
                # Create Ticket with fare details.
                ticket = Ticket(location)
                receipt = ticket.printTicket("Entry")
            else:
                raise CustomException("CarWithSameNumExist")
        except Exception as e:
            return e.value
        else:
            return receipt

    def displayCars(self):
        ''' This method diplays all the cars that are parked.'''
        carDetailsDict = {"cars": []}
        for car in carDataDetails.objects.values("carno",
                                                 "tariff_plan",
                                                 "location", "inTime"):
            # Retrieve and return each car details parked in
            # the parking station.
            car["inTime"] = Ticket.convert_time_format(car["inTime"])
            carDetailsDict["cars"].append(car)
        if len(carDetailsDict['cars']) == 0:
            carDetailsDict['code'] = 204
        else:
            carDetailsDict['code'] = 200
        return carDetailsDict

    def __assignSpot(self):
        '''This method assigns an available spot to the car
           in the specified level.
        '''
        assignedSpot = None
        levels = ParkingLevel.objects.all()
        if levels.count() == 0:
            # Check whether atleast one parking level exist.
            raise CustomException("ParkingLevelDoesntExist")
        for level in levels:
            # Searching for free spots in each parking level.
            free_spots = ast.literal_eval(level.free_spots)
            if len(free_spots) > 0:
                # Assign from lowest parking spot in this specific level
                # if free spots available.
                assignedSpot = free_spots[0]
                # Remove a assigned spot from free spots and update the db.
                free_spots.remove(int(assignedSpot))
                level.free_spots = str(free_spots)
                # Add assigned spot in the occupied spots and update the db.
                occupiedSlots = ast.literal_eval(level.occupied_spots)
                occupiedSlots.append(assignedSpot)
                level.occupied_spots = str(occupiedSlots)
                level.save()
                break
        # Raise an exception if no space left in any of the parking level.
        if assignedSpot is None:
            raise CustomException("NoSpaceLeftInParking")
        else:
            return assignedSpot

    def __unAssignSpot(self, location):
        '''This method un assigns occpied spot of the car at exit.'''
        # Loop over all the parking levels to find out the spot.
        for level in ParkingLevel.objects.all():
            # Fetch the occipied spots of the specific level.
            occupiedSlots = ast.literal_eval(level.occupied_spots)
            # Check whether the location specified exist in the occupied spots.
            if int(location) in occupiedSlots:
                # If found remove the spot from assigned and add in free spots.
                free_spots = ast.literal_eval(level.free_spots)
                free_spots.insert(0, int(location))
                level.free_spots = str(free_spots)
                occupiedSlots.remove(int(location))
                level.occupied_spots = str(occupiedSlots)
                level.save()
                break

    def removeCar(self, location):
        ''' This method removes a car based on specific location
            from the parking space and make it available for next cars.
        '''
        try:
            # Delete the car entry if exist otherwise raise an exception.
            if carDataDetails.objects.filter(location=location).count() == 0:
                raise CustomException("NoCarFound")

            # Create Ticket with fare details.
            ticket = Ticket(location)
            receipt = ticket.printTicket("Exit")
            carDataDetails.objects.get(location=location).delete()
            # Delete the car object from database.
            # Unassign or free the occipied spot of the car.
            self.__unAssignSpot(location)
        except Exception as e:
            return e.value
        else:
            return receipt
