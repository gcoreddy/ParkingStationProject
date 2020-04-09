class NoSpaceLeftInParking(Exception):
    '''Exception for no space left in the parking.'''
    pass

class CarWithSameNumExist(Exception):
    '''Exception if car is already parked with the same number.'''
    pass

class LocationEmpty(Exception):
    '''Exception if user tries to remove a parking slot which is not occupied.'''
    pass

class NoCarFound(Exception):
    '''Exception if there is no car with the name specified.'''
    pass
	
class InvalidTariff(Exception):
    '''Exception if user selects invalid tariff plan.'''
    pass
	
class NoCarstoDisplay(Exception):
    '''Exception if there are no cars exists in the parking.'''
    pass
	
class LevelWithTheSameName(Exception):
    '''Exception while creating a new level.
	   throws an exception if there is a level with the same name exist'''
    pass
	
class TariffPlanDoesntExist(Exception):
    '''Exception if there is no tariffPlan defined.'''
    pass
	
class MultipleCarsWithSameLocation(Exception):
    '''Exception if database shows multiple cars with the same location spot'''
    pass
	
class ParkingLevelDoesntExist(Exception):
    '''Exception if there is no Parking level exist in the station.'''
    pass
	
parkingExceptionsDict = {
             "NoSpaceLeftInParking"  : { "status" : "Error",
			                             "code"   : 404,
			                              "Reason" : "No Space left in the parking."
							           },
			  "CarWithSameNumExist" : { "status" : "Error",
			                            "code"   : 404,
			                             "Reason" : "Car with same number already exist in the parking."
									   },
			  "LocationEmpty"       :  { "status" : "Error",
			                             "code"   : 404,
                                         "Reason" : "Specified parking location is already empty."			  
									   },
			  "NoCarFound"          :  { "status" : "Error",
			                             "code"   : 404,
			                             "Reason" : "No cars found in the parking. Parking is empty."
										},
			  "InvalidTariff"        :  { "status" : "Error",
                                          "code"   : 400,
			                              "Reason" : "Traiff Plan selected is invalid."
										},
			   "NoCarstoDisplay"     :  { "status" : "Success",
                                           "code"   : 204,
			                              "Message" : "Parking station doesn't have parked cars."
			                           },
			    "LevelWithTheSameName" : { "status" : "Error",
				                           "Reason" : "Level with the same name already exist."
										},
				"TariffPlanDoesntExist" : {"status" : "Error",
                                            "code"   : 404,
				                           "Error"  : "Tariff Plan is not yet defined in the database."
				                        },
	  "MultipleCarsWithSameLocation" : { "status" : "Error",
				                         "Error" : "Multiple cars are assigned with same location Number."
			                            },
			"ParkingLevelDoesntExist" : { "status" : "Error",
                                          "code"   : 404,
			                             "Error"  : "Parking Level doesn't exist or not yet added."
	                                    },
			"UnExpectedError"         : {"status" : "Error",
                                         "code"   : 400,
			                             "Error"  :  "Unexpected error occured"
										 },
	}