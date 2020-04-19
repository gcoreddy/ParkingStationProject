import time
import sys
from parking.models import TariffPlan
from parking.src.common import CustomException


class CalCulateCost:
    '''Calculates the cost based on plan and suggests a better
        plan to user, if user not opted for prpoer plan.
    '''

    def __get_tariffplan_cost(self, tariff_plan):
        '''Validates whether tariff plan exist or not in our database.'''
        if TariffPlan.objects.filter(tariff_plan=tariff_plan).count() == 0:
            # Raise exception if not found.
            raise CustomException("TariffPlanDoesntExist")
        else:
            # Return the cost of the specific plan.
            return TariffPlan.objects.get(tariff_plan=tariff_plan).cost

    def hourCal(self, minutes, hours):
        '''Calculates the cost based on hourly plan.'''
        newPlan = "hourly"
        # Get the cost base on the plan.
        newCost = self.__get_tariffplan_cost(newPlan)
        # Add 1 if there exists minutes to treat that as new hour.
        if minutes > 0:
            hours += 1
        # Calculate the cost as per hours and cost.
        return (newPlan, newCost * hours)

    def daysCal(self, minutes, hours, days):
        '''Calculates the cost based on daily plan.'''
        newPlan = "daily"
        # Get the cost base on the plan.
        newCost = self.__get_tariffplan_cost(newPlan)
        # Add 1 if there exists minutes or hours to treat that as new day.
        if hours > 0 or minutes > 0:
            days += 1
        # Calculate the cost as per hours and cost.
        return (newPlan, newCost * days)

    def weeksCal(self, minutes, hours, days, weeks):
        '''Calculates the cost based on weekly plan.'''
        newPlan = "weekly"
        # Get the cost base on the plan.
        newCost = self.__get_tariffplan_cost(newPlan)
        # Add 1 if there exists minutes or hours or day to treat
        # that as new week.
        if hours > 0 or minutes > 0 or days > 0:
            weeks += 1
        # Calculate the cost as per hours and cost.
        return (newPlan, newCost * weeks)

    def mnthsCal(self, minutes, hours, days, weeks, months):
        '''Calculates the cost based on monthly plan.'''
        newPlan = "monthly"
        # Get the cost base on the plan.
        newCost = self.__get_tariffplan_cost(newPlan)
        # Add 1 if there exists minutes or hours or day or weeks to treat
        # that as new month.
        if minutes > 0 or days > 0 or hours > 0 or weeks > 0:
            months += 1
        # Calculate the cost as per hours and cost.
        return (newPlan, newCost * months)

    def calculate_cost(self, plan, minutes=0, hours=0, days=0,
                       weeks=0, months=0):
        '''Calculates the cost based on plan.'''
        if plan == "monthly":
            plan, cost = self.mnthsCal(minutes, hours, days, weeks, months)
        elif plan == "weekly":
            if months != 0:
                weeks += 4*months
            plan, cost = self.weeksCal(minutes, hours, days, weeks)
        elif plan == "daily":
            if months != 0:
                days += 30*months
            if weeks != 0:
                days += 7*weeks
            plan, cost = self.daysCal(minutes, hours, days)
        elif plan == "hourly":
            if months != 0:
                hours += 24*30*months
            if weeks != 0:
                hours += 24*7*weeks
            if days != 0:
                hours += 24*days
            plan, cost = self.hourCal(minutes, hours)
        return cost

    def tariffCalculator(self, tariff_plan, carTT):
        months = carTT//(60*60*24*30)
        if months:
                carTT -= months * (60*60*24*30)
        weeks = carTT//(60*60*24*7)
        if weeks:
            carTT -= months * (60*60*24*7)
        days = carTT//(60*60*24)
        if days:
                carTT -= days * (60*60*24)
        hours = (carTT//(60*60))
        if hours:
                carTT -= hours * (60*60)
        minutes = carTT//60
        tPlan = TariffPlan.objects.get(tariff_plan=tariff_plan)
        currentPlan = tPlan.tariff_plan
        oldCost = tPlan.cost
        oldPlan = tPlan.tariff_plan
        freetime = tPlan.freetime
        newPlan = ""
        newCost = 0
        if days == 0 and weeks == 0 and months == 0:
            # If total time within hours.
            if hours == 0 and minutes <= freetime:
                # If total time is less than free time.
                print("Car inside for less than free minutes so cost: 0")
            # Calculate cost as per current plan of the user.
            # Calculate the cost as per the suggested plan.
            newPlan, newCost = self.hourCal(minutes, hours)
            oldCost = self.calculate_cost(currentPlan, minutes)
        elif days < 7 and weeks == 0 and months == 0:
            # If days are less than 7 and weeks and months are 0 then
            # This falls into daily plan.
            newPlan, newCost = self.daysCal(minutes, hours, days)
            oldCost = self.calculate_cost(currentPlan, minutes, hours, days)
        elif days < 30 and weeks != 0 and months == 0:
            # If days are less than 30 and months are 0 then
            # This falls into weekly plan.
            newPlan, newCost = self.weeksCal(minutes, hours, days, weeks)
            oldCost = self.calculate_cost(currentPlan, minutes,
                                          hours, days, weeks)
        else:
            # If days are more than 30 then falls into monthly plan.
            newPlan, newCost = self.mnthsCal(minutes, hours, days,
                                             weeks, months)
            oldCost = self.calculate_cost(currentPlan, minutes,
                                          hours, days, weeks, months)

        if newPlan == "":
            print("You have stayed only 15 min fee is : 0")
            return (oldPlan, 0)
        elif newCost < oldCost:
            print("Your plan is not appropiate pls select the plan:", newPlan)
            return (newPlan, newCost)
        else:
            print("Your plan is accurate:", oldPlan)
            return (oldPlan, oldCost)
