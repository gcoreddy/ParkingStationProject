import time
from parking.models import TariffPlan, carDataDetails
from parking.src.common import CustomException


class Ticket:

    ''' Class used for update/create tariff plans and for
        generating tickets with fare details for cars at exit.'''

    def __init__(self, location):
        '''Constructor method'''
        self.outTime = time.time()
        self.carno = None
        self.inTime = 0
        self.freetime = 15
        self.location = location
        self.tariff = None
        self.cost = 0
        self.ID = self.__generateTicketID()
        self.amount = None
        self.tariffMinutesDict = {
                                  "Hourly": 3600,
                                  "Daily": 86400
                                 }

    def __fill_car_details(self, location):
        ''' This method searches and returns in the database for car
            based on location details provided'''
        car = carDataDetails.objects.get(location=location)
        self.carno = car.carno
        self.inTime = car.inTime
        self.tariff = car.tariff_plan.tariff_plan
        self.freetime = car.tariff_plan.freetime
        self.cost = car.tariff_plan.cost

    def __generateTicketID(self):
        ''' Generates a random id for a ticket'''
        import random
        ID = random.randint(1, 1000)
        return ID

    def __calculate_amount(self):
        ''' Method calculates the amount for the car at exit based on
            intime,outtime and tariff plan selected at entry.'''

        # Get the cost and free time for the specific tariff plan.
        if (self.outTime - self.inTime) < float(self.freetime)*60:
            # Return 0 if the outtime is less then the freetime of the plan.
            return 0
        else:
            # Calculate the total time of stay of a car minus free minutes
            # multiplied by cost.
            tariffMnts = self.tariffMinutesDict[self.tariff]
            totalTime = self.outTime - self.inTime - float(self.freetime)*60
            price = (totalTime//int(tariffMnts)+1) * int(self.cost)
            return price

    def create_tariff(plan_name, plan_cost, plan_freetime):
        ''' Creates a new tariff plan.'''
        tarifPlansDict = {"TariffPlansInfo": []}
        if TariffPlan.objects.filter(tariff_plan=plan_name).count() == 0:
            newPlan = TariffPlan(tariff_plan=plan_name, cost=plan_cost,
                                 freetime=plan_freetime)
            newPlan.save()
            return Ticket.display_tariff()
        else:
            return CustomException("TariffPlanAlreadyExist").value

    def update_tariff(plan_name, plan_cost, plan_freetime):
        ''' Creates or updates the tariff plan details.'''
        tarifPlansDict = {"TariffPlansInfo": []}
        if TariffPlan.objects.filter(plan=plan_name).count() > 0:
            existingPlan = TariffPlan.objects.get(plan=plan_name)
            existingPlan.cost = plan_cost
            existingPlan.freetime = plan_freetime
            existingPlan.save()
            return Ticket.display_tariff()
        else:
            raise CustomException("TariffPlanDoesntExist")

    def display_tariff(self):
        # Display all the existing tariff plan details.
        for plan in TariffPlan.objects.all().values("plan", "cost",
                                                    "freetime"):
            tarifPlansDict["TariffPlansInfo"].append(plan)
        tarifPlansDict["status"] = "Success"
        tarifPlansDict["code"] = 200
        return tarifPlansDict

    def printTicket(self, point):
        """Prints the ticket at entry and exit also calculates
           the fare as well at exit."""
        self.__fill_car_details(self.location)
        ticketDict = {"Car": self.carno, "tariff": self.tariff,
                      "Location": self.location, "ID": self.ID,
                      "Start": time.strftime("%m/%d/%Y, %H:%M:%S",
                                             time.gmtime(float(self.inTime)))}
        if point == "Exit":
            # Calling calulate method to get the cost for the user.
            self.amount = self.__calculate_amount()
            ticketDict["Finish"] = time.strftime("%m/%d/%Y, %H:%M:%S",
                                              time.gmtime(float(self.outTime)))
            ticketDict["Fee"] = self.amount
        ticketDict["status"] = "Success"
        ticketDict["code"] = 200
        return ticketDict
