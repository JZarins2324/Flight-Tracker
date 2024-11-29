import db
from business import Passenger, Plane, Flight

# Number of dashes displayed in view functions
NUM_DASHES = 130

def display_title():
    print("FLIGHT MANAGER\n")

def display_menu():
    # I abbreviated the menu commands since writing out commands like, "view_passenger_by_flight" would be inconvenient and prone to typos.
    print("COMMAND MENU")
    print("vf - view all flights")
    print("vpf - view all passengers on a flight")
    print("vp - view all passengers with the given last name")
    print("vpl - view the plane used for a flight")
    print("vpls - view all planes")
    print("cf - create a flight")
    print("cp - create a passenger")
    print("cpl - create a plane")
    print("ap - assign a passenger to a flight")
    print("menu - display the menu")
    print("exit - exit program")
    print()

def view_flights(flights:list[Flight]):
    if len(flights) == 0:
        print("No flights to view")
        return
    
    print("FlightID\tPlaneID\tSTD\t\t\tSTA\t\t\tOrigin\tDestination\tMiles Travelled\tCapacity")
    print("-" * NUM_DASHES)
    for flight in flights:
        print(f"{flight.id}\t\t{flight.plane.id}\t{flight.start_time}\t{flight.arrival_time}\t{flight.origin}\t{flight.destination}\t\t{flight.miles_travelled}\t\t{len(flight.passengers)}/{flight.plane.capacity}")
    print("-" * NUM_DASHES)
    print()

def view_passengers(passengers:list[Passenger]):
    if len(passengers) == 0:
        print("No passengers to view")
        return
    
    print("PassengerID\tFirst Name\tLast Name\tPhone\t\tEmail\t\t\tAddress")
    print("-" * NUM_DASHES)
    for passenger in passengers:
        print(f"{passenger.id}\t\t{passenger.first_name}\t\t{passenger.last_name}\t\t{passenger.phone}\t{passenger.email}\t\t{passenger.address}")
    print("-" * NUM_DASHES)
    print()

def view_planes():
    planes = db.get_planes()

    if len(planes) == 0:
        print("No planes to view")
        return
    
    print("PlaneID\tMake\tModel\tCapacity\tAge")
    print("-" * NUM_DASHES)
    for plane in planes:
        print(f"{plane.id}\t{plane.make}\t{plane.model}\t{plane.capacity}\t\t{plane.age}")
    print("-" * NUM_DASHES)
    print()

def view_plane(flight_id):
    plane = db.get_plane(flight_id)

    if plane:
        print("PlaneID\tMake\tModel\tCapacity\tAge")
        print("-" * NUM_DASHES)
        print(f"{plane.id}\t{plane.make}\t{plane.model}\t{plane.capacity}\t\t{plane.age}")
        print("-" * NUM_DASHES)
    else:
        print("No plane to view")
    print()

def create_flight():
    flight = Flight()
    
    flight.plane = db.get_plane(input("Enter the plane's ID: "))
    flight.passengers = []
    flight.start_time = input("Enter take-off time: ")
    flight.arrival_time = input("Enter arrival time: ")
    flight.origin = input("Enter the origin of the flight: ")
    flight.destination = input("Enter the destination of the flight: ")
    flight.miles_travelled = input("Enter how many miles the plane travelled: ")
    print()

    db.save_flight(flight)

def create_plane():
    plane = Plane()

    plane.make = input("Enter plane's Make: ")
    plane.model = input("Enter plane's Model: ")
    plane.capacity = input("Enter plane's Capacity: ")
    plane.age = input("Enter plane's age: ")
    print()

    db.save_plane(plane)

def create_passenger():
    passenger = Passenger()

    passenger.first_name = input("Enter passenger's first name: ")
    passenger.last_name = input("Enter passenger's last name: ")
    passenger.phone = input("Enter passenger's phone number: ")
    passenger.email = input("Enter passenger's email: ")
    passenger.address = input("Enter passenger's address: ")
    print()

    db.save_passenger(passenger)

def assign_passenger():
    passenger_id = input("Enter the passenger's ID: ")
    flight_id = input("Enter the flight ID: ")

    # Get the corresponding flight
    flight = db.get_flight(flight_id)

    db.assign_passanger(passenger_id, flight_id)
    flight.add_passenger(db.get_passenger_by_id(passenger_id))
    print()

def main():
    display_title()
    display_menu()

    db.connect()

    while True:
        command = input("Enter a command: ").lower()
        if command == "vf":
            flights = db.get_flights()
            if flights == None:
                flights = []

            view_flights(flights)
        elif command == "vpf":
            id = input("Enter the flight's id: ")
            view_passengers(db.get_passengers(id))
        elif command == "vp":
            last_name = input("Enter a last name: ")
            view_passengers(db.get_passengers_by_name(last_name))
        elif command == "vpl":
            id = input("Enter the planes's id: ")
            view_plane(id)
        elif command == "vpls":
            view_planes()
        elif command == "cf":
            create_flight()
        elif command == "cp":
            create_passenger()
        elif command == "cpl":
            create_plane()
        elif command == "ap":
            assign_passenger()
        elif command == "menu":
            display_menu()
        elif command == "exit":
            break
        else:
            print(f"'{command}' is an invalid command\n")
            display_menu()

main()