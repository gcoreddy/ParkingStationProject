# parkingStationProject
parking station implementation in rest as well as web

Pre requisites:
===============
1. Python 3.6 or above. 
2. Django should be installed on the machine.

Starting the application:
=========================
1. Clone the project to local folder.
2. Go to the folder parkingStationProject.

3. Run the command "python manage.py createsuperuser" which creates a super users, by using which we can perform adminstrative operations.


4. Run the command "python manage.py makemigrations" to create database models.

5. Run the command "python manage.py migrate" migrates database tables.

6. Start the application using the command. "python manage.py runserver" which starts the webserver on specified ip and port.

By default application starts on "127.0.0.1:8000". If user wants to provide different ip and port they have to pass these as an arguments to manage.py while starting.

Ex: python manage.py runserver 192.168.67.1:9000

How to Use through web api:
============================
Open the link in browser. Multiple options will be available to select.

1. update_tariff - is useful to add or update any tariff plan (This will be enabled only for admin user. Normal user can't perform this operation.).

2. addCar --- is useful to add a car to the parking slot. After addition generates a ticket with the details.

3. removeCar ---- this is useful to unassign spot for a car and generate ticket with cost. 4 .displayCars ----- Displays list of cars parked.
4. addLevel --- This option enables the user to expand the parking levels (This option will be privided only to the admin users.)

How to performs Admin tasks:
============================

Admin page can be accessed by calling http://ip:port/admin and we have to provide superuser credentials we created. After login it shows the database models we define in the models.py. We can add modify or delete the info of any model exist in the database. We can create and delete users etc. Using this we can perform any admin task related to the application.

How to use through rest api:
==============================
There are 3 GET operations provided for rest api.

1. add
2. remove
3. list

http://host:port/add?car=X774HY98&tariff=hourly

{"status": "success", "car": "X774HY98", "tariff": "hourly", "location": 12, "start": "2014-10-01 14:11:45"} <-- info to print ticket for driver on entrance.

http://host:port/add?car=X774HY98&tariff=daily

{"status": "error", "No free space"} <-- info to show on display of ticket machine for driver.

http://host:port/remove?location=12

{"status": "success", "start": "2014-10-01 14:11:45", "finish": "2014-10-01 14:21:57", "location": 12, "car": "X774HY98", "fee": 0, "tariff": "hourly"} <-- info to print receipt for driver on exit.

http://host:port/list

{"status": "success", "cars" : [

{"car": "X774HY98", "tariff": "hourly", "location": 1, "start": "2014-10-01 14:11:45"},

{"car": "X637TT98", "tariff": "daily", "location": 2, "start": "2014-10-01 15:23:05"}
] } <-- info to parking administrator.
