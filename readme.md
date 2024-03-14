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
13. We have a Audit table for Cabs which can be viewed in the database or in the django admin panel


Contract for all the APIs with example can be found in the shared postman collection


## Assumptions:
1. While booking a cab whichever cab have the highest idle time will be booked.
2. As soon as cab is booked the trip is started. As sheduling the cab was not in the scope of problem
3. While getting the idle time for cabs if the cab is on trip the end time will be equal to the given end time


## How to run?

{pip3 install -r requirements.txt}
