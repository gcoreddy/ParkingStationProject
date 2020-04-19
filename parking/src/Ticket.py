import time
import sys
from parking.models import TariffPlan, carDataDetails
from parking.src.common import CustomException
from parking.src.CalculateTariff import CalCulateCost


class Ticket(CalCulateCost):

    ''' Class used for update/create tariff plans and for
        generating tickets with fare details for cars at exit.'''

    def __init__(self, location):
        '''Constructor method'''
        self.outTime = time.time()
        self.carno = None
        self.inTime = 0
        self.freetime = 15
        self.location = location
        self.tariff_plan = None
        self.cost = 0
        self.ID = self.__generateTicketID()
        self.amount = None

    def __fill_car_details(self, location):
        ''' This method searches and returns in the database for car
            based on location details provided'''
        car = carDataDetails.objects.get(location=location)
        self.carno = car.carno
        self.inTime = car.inTime
        self.tariff_plan = car.tariff_plan.tariff_plan
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
        # Calculate the total time stayed in car.
        totalTime = self.outTime - self.inTime
        # Calculate the cost and suggested plan for the user.
        plan, price = self.tariffCalculator(self.tariff_plan, totalTime)
        return (plan, price)

    def display_tariff():
        # Display all the existing tariff plan details.
        tarifPlansDict = {"TariffPlansInfo": []}
        for plan in TariffPlan.objects.all().values("tariff_plan", "cost",
                                                    "freetime"):
            tarifPlansDict["TariffPlansInfo"].append(plan)
        tarifPlansDict["status"] = "Success"
        tarifPlansDict["code"] = 200
        return tarifPlansDict

    def create_tariff(plan_name, plan_cost, plan_freetime):
        ''' Creates a new tariff plan.'''
        # Check the tariff plan doesn't exist in the database.
        if TariffPlan.objects.filter(tariff_plan=plan_name).count() == 0:
            newPlan = TariffPlan(tariff_plan=plan_name, cost=plan_cost,
                                 freetime=plan_freetime)
            newPlan.save()
            return Ticket.display_tariff()
        else:
            # Raise an exception plan already exist in db.
            return CustomException("TariffPlanAlreadyExist").value

    def update_tariff(plan_name, plan_cost, plan_freetime):
        ''' Creates or updates the tariff plan details.'''
        tarifPlansDict = {"TariffPlansInfo": []}
        # Checking whether the plan exist or not.
        if TariffPlan.objects.filter(tariff_plan=plan_name).count() > 0:
            # Get the existing tariff plan object.
            existingPlan = TariffPlan.objects.get(tariff_plan=plan_name)
            # Update the db with new values.
            existingPlan.cost = plan_cost
            existingPlan.freetime = plan_freetime
            # Save the new values.
            existingPlan.save()
            # Display the details to the user.
            displayDict = Ticket.display_tariff()
            return displayDict
        else:
            # Raise Custome exception if the plan doesn't exist.
            return CustomException("TariffPlanDoesntExist").value

    def convert_time_format(tme):
        # Convert time format to Human Readable format.
        return time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime(tme))

    def printTicket(self, point):
        """Prints the ticket at entry and exit also calculates
           the fare as well at exit."""
        self.__fill_car_details(self.location)
        ticketDict = {
                      "Car": self.carno,
                      "Location": self.location, "ID": self.ID,
                      "Start": Ticket.convert_time_format(self.inTime)
                     }
        if point == "Exit":
            # Calling calulate method to get the cost for the user.
            self.tariff_plan, self.amount = self.__calculate_amount()
            # Update the db with the suggested tariff plan by algorithm.
            ticketDict["tariff"] = self.tariff_plan
            ticketDict["Finish"] = Ticket.convert_time_format(self.outTime)
            ticketDict["Fee"] = self.amount
        ticketDict["status"] = "Success"
        ticketDict["code"] = 200
        return ticketDict
