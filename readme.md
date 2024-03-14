# Cab portal management service

This project have following features
1. Register a Cab
2. Onboard a city
3. Book a Cab(start trip)
4. End a trip
5. Get all bookings
6. Get all bookings by cab/city
7. Get all city
8. Get city by Id
9. Get all cabs
10. Get cab by Id
11. Get Idle cab Duration
12. Get highest city in demand and also the peak hour where booking were highest
13. We have a Audit table for Cabs which can be viewed in the database or the django admin panel


Contract for all the APIs with example can be found in the shared [Postman collection](https://github.com/itachi0071998/cab-managment-portal/blob/main/CMP%20Collection.postman_collection.json)


## Assumptions:
1. While booking a cab whichever cab has the highest idle time will be booked.
2. As soon as a cab is booked the trip is started. As scheduling the cab was not in the scope of the problem
3. While getting the idle time for cabs if the cab is on a trip the end time will be equal to the given end time


## How to run?

```
pip3 install -r requirements.txt
```
we will migrate now
```
python3 manage.py migrate
```
Now, its time to create a super user to access the [admin panel](http://127.0.0.1:8000/admin/)
```
python3 manage.py createsuperuser --username admin --email admin@example.com
```

Now, its time to start the server
```
python3 manage.py runserver
```



