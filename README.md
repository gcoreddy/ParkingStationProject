# parkingStationProject
parking station implementation in rest as well as web
parking station implementation in django

Pre requisites:
================
1. Python 3.6 or above. 
2. Django should be installed on the machine.
3. Sqlit3 database which is default in Django.


Starting the application:
=========================
1. Clone the gitrepo and goto the directory

2. Run the command "python manage.py createsuperuser" which creates a super users, by using which we can perform adminstrative operations.

3. Run the command "python manage.py makemigrations" to create database models.

4. Run the command "python manage.py migrate --run-syncdb" migrates database tables.

5. Start the application using the command. "python manage.py runserver" which starts the webserver on specified ip and port.

By default application starts on "127.0.0.1:8000". If user wants to provide different ip and port they have to pass these as an arguments to manage.py while starting.

Ex: python manage.py runserver 192.168.67.1:9000


Architecture:
=============
Model-View-Template for Web API.
Model–view–viewmodel for REST API.
ORM (Object-Relational-Mapper) for database models.
Project implemented in Object oriented manner.


Web page implementation:
========================
Web api is implemented in Model-View-Template architectural design.
The MVT (Model View Template) is a software design pattern. It is a collection of three important components Model View and Template. The Model helps to handle database. It is a data access layer which handles the data. The Template is a presentation layer which handles User Interface part completely.

How to Use:
============
Open the link in browser. 
Multiple options will be available to select.

1. add_tariff - Is useful to add or update any tariff plan (This will be enabled only for admin user. Normal user can't perform this operation.).
2. update_tariff - Is useful to update any tariff plan (This will be enabled only for admin user. Normal user can't perform this operation.).
3. addCar --- is useful to add a car to the parking slot. After addition generates a ticket with the details.
4. removeCar ---- this is useful to unassign spot for a car and generate ticket with cost. 4 .displayCars ----- Displays list of cars parked.
5. addLevel --- This option enables the user to expand the parking levels (This option will be privided only to the admin users.).
6. displayCars --- This option is useful for displaying the cars that are there in the parking station.

How to performs Admin tasks:
=============================
1. Admin page can be accessed by calling http://ip:port/admin.
2. We have to provide superuser credentials we created. 
3. After logging in, it shows the database models we defined in the models. 
4. We can add,modify,display or delete the info of any model exist in the database. 
5. We can create and delete users etc. Using this we can perform any admin task related to the application.

Rest API Implementation:
=========================
Rest api is implemented in Model-View-Model Architecture using Django.
Model–view–viewmodel (MVVM) is a software architectural pattern that facilitates the separation of the development of the graphical user interface (the view) – be it via a markup language or GUI code – from the development of the business logic or back-end logic (the model) so that the view is not dependent on any specific model platform. The view model of MVVM is a value converter,[1] meaning the view model is responsible for exposing (converting) the data objects from the model in such a way that objects are easily managed and presented. In this respect, the view model is more model than view, and handles most if not all of the view's display logic.[1] The view model may implement a mediator pattern, organizing access to the back-end logic around the set of use cases supported by the view.
There are 3 options provided for rest api.

Add car rest api invocation:
============================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/add?car_num=abc123&tariff_plan="Hourly"
{"Car": "abc123", "tariff": "Hourly", "Location": "L1_8", "ID": 668, "Start": "04/15/2020, 14:20:15", "status": "Success", "code": 200}

Try to add a car which is already there in the parking:
=========================================================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/add?car_num=abc123&tariff_plan="Hourly"
{"status": "Error", "code": 404, "Reason": "Car with same number already exist in the parking."}

Add car response if Tariff plan not defined in the database:
=============================================================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/add?car_num=abc&tariff_plan="Daily"
{"status": "Error", "code": 404, "Error": "Tariff Plan is not yet defined in the database."}

Add car response when parking is already full:
==============================================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/add?car_num=abc31234&tariff_plan="Hourly"
{"status": "Error", "code": 404, "Reason": "No Space left in the parking."}


Remove Car rest api invocation:
===============================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/remove?location=L1_5
{"Car": "sad;ksd", "tariff": "Hourly", "Location": "L1_5", "ID": 481, "Start": "04/15/2020, 13:56:31", "Finish": "04/15/2020, 15:38:04", "Fee": 20.0, "status": "Success", "code": 200}

Remove Car from a location which is empty:
===========================================
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/remove?location=L1_5
{"status": "Error", "code": 404, "Reason": "No cars found in the specified location. Parking slot is empty."}


displayCars:
==============
C:\Users\cgavired>curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/list
{"cars": [{"carno": "sajkkads", "tariff_plan": "Hourly", "location": "L1_7", "inTime": "04/15/2020, 13:56:06"}, {"carno": "sadkjasd", "tariff_plan": "Hourly", "location": "L1_4", "inTime": "04/15/2020, 13:56:39"}, {"carno": "ksadjl", "tariff_plan": "Hourly", "location": "L1_3", "inTime": "04/15/2020, 13:56:45"}, {"carno": "asdkjsad", "tariff_plan": "Hourly", "location": "L3_10", "inTime": "04/15/2020, 13:57:05"}, {"carno": "abc123", "tariff_plan": "Hourly", "location": "L1_8", "inTime": "04/15/2020, 14:20:15"}, {"carno": "abc1234", "tariff_plan": "Hourly", "location": "L1_5", "inTime": "04/15/2020, 15:40:55"}], "code": 200}


Output format:
================
In both Web and Rest api response will be displayed in the form of JSON.
1. Response contains status, status code, reason incase of failre or data in case of success.
2. Implemented different error codes in response (200,201,404,401 etc)


Exception Handling:
===================
1. Created a separate class custom class for hadling all type of exceptions.
2. This will print the response json based on exception we get.
3. Handled all different types of exceptions like negative testing related.

Not Implemented Tasks:
========================
User registration and login is not handled as that is not there in the scope.
Users an access only admin page, which is by default comes with Django.

