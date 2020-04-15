		
class CustomException(Exception):
    # Constructor or Initializer 
    def __init__(self, value):
        self.value = parkingExceptionsDict[value]
  
    # __str__ is to print() the value 
    def __str__(self):
        return repr(self.value)
	
parkingExceptionsDict = {
             "NoSpaceLeftInParking"  : { "status" : "Error",
			                             "code"   : 404,
			                              "Reason" : "No Space left in the parking."
							           },
			  "FailedCreateParkingLevel" : { "status" : "Error",
			                             "code"   : 400,
										 "Reason" : "Unable to create Parking Level"
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
			                             "Reason" : "No cars found in the specified location. Parking slot is empty."
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
				"TariffPlanAlreadyExist" : {"status" : "Error",
                                            "code"   : 404,
				                           "Error"  : "Tariff Plan already exist with in the database."
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