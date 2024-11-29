from business import Passenger, Plane, Flight
import sqlite3
from contextlib import closing

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "Final.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

#
# These functions query the DB to get planes
#
def get_plane(plane_id=0):
    try:
        query = """
        SELECT PlaneID, Make, Model, Capacity, Age
        FROM planes
        WHERE PlaneID = ?
        """

        with closing(conn.cursor()) as c:
            c.execute(query, (plane_id,))
            row = c.fetchone()

            if row:
                plane = Plane()

                plane.id = row["PlaneID"]
                plane.make = row["Make"]
                plane.model = row["Model"]
                plane.capacity = row["Capacity"]
                plane.age = row["Age"]

                return plane
            return False
    except sqlite3.OperationalError:
        return False
    

def get_planes():
    try:
        query = """
        SELECT PlaneID, Make, Model, Capacity, Age
        FROM planes
        """

        with closing(conn.cursor()) as c:
            c.execute(query)
            rows = c.fetchall()

            planes = []
            for row in rows:
                plane = Plane()

                plane.id = row["PlaneID"]
                plane.make = row["Make"]
                plane.model = row["Model"]
                plane.capacity = row["Capacity"]
                plane.age = row["Age"]

                planes.append(plane)
            return planes
    except sqlite3.OperationalError:
        return False

#
# These functions query the DB to get flights
#
def get_flights():
    query = """
    SELECT FlightID, PlaneID, STD, STA, Origin, Destination, MilesTravelled
    FROM flights
    """

    with closing(conn.cursor()) as c:
        c.execute(query)
        rows = c.fetchall()

        flights = []
        for row in rows:
            flight = Flight()
            flight.id = row["FlightID"]
            flight.plane = get_plane(row["PlaneID"])
            flight.start_time = row["STD"]
            flight.arrival_time = row["STA"]
            flight.origin = row["Origin"]
            flight.destination = row["Destination"]
            flight.miles_travelled = row["MilesTravelled"]

            ids = get_passenger_ids(flight.id)

            for id in ids:
                flight.passengers.append(get_passenger_by_id(id))

            flights.append(flight)
        return flights
    

def get_flight(id):
    query = """
    SELECT FlightID, PlaneID, STD, STA, Origin, Destination, MilesTravelled
    FROM flights
    WHERE FlightID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        rows = c.fetchall()

        flight = Flight()
        for row in rows:
            flight.id = row["FlightID"]
            flight.plane = get_plane(row["PlaneID"])
            flight.start_time = row["STD"]
            flight.arrival_time = row["STA"]
            flight.origin = row["Origin"]
            flight.destination = row["Destination"]
            flight.miles_travelled = row["MilesTravelled"]

        return flight
    
#
# These functions query the DB to get the passengers
#
def get_passengers(flight_id):
    query = """
    SELECT PassengerID, FirstName, LastName, PhoneNumber, Email, Address
    FROM passengers
    WHERE PassengerID IN (
        SELECT PassengerID
        FROM passengerToFlights
        WHERE FlightID = ?
    );
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (flight_id,))
        rows = c.fetchall()

        passengers = []
        for row in rows:
            passenger = Passenger()

            passenger.id = row["PassengerID"]
            passenger.first_name = row["FirstName"]
            passenger.last_name = row["LastName"]
            passenger.phone = row["PhoneNumber"]
            passenger.email = row["Email"]
            passenger.address = row["Address"]

            passengers.append(passenger)

        return passengers


def get_passengers_by_name(last_name):
    query = """
    SELECT PassengerID, FirstName, LastName, PhoneNumber, Email, Address
    FROM passengers
    WHERE LastName = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (last_name,))
        rows = c.fetchall()

        passengers = []
        for row in rows:
            passenger = Passenger()

            passenger.id = row["PassengerID"]
            passenger.first_name = row["FirstName"]
            passenger.last_name = row["LastName"]
            passenger.phone = row["PhoneNumber"]
            passenger.email = row["Email"]
            passenger.address = row["Address"]

            passengers.append(passenger)

        return passengers
    

def get_passenger_by_id(id):
    query = """
    SELECT PassengerID, FirstName, LastName, PhoneNumber, Email, Address
    FROM passengers
    WHERE PassengerID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        row = c.fetchone()

        passenger = Passenger()

        passenger.id = row["PassengerID"]
        passenger.first_name = row["FirstName"]
        passenger.last_name = row["LastName"]
        passenger.phone = row["PhoneNumber"]
        passenger.email = row["Email"]
        passenger.address = row["Address"]

        return passenger


def get_passenger_ids(flight_id):
    query = """
        SELECT PassengerID
        FROM passengerToFlights
        WHERE FlightID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (flight_id,))
        rows = c.fetchall()

        ids = []

        for row in rows:
            ids.append(row["PassengerID"])

        return ids
#
# These functions insert values the user entered into the DB
#
def save_plane(plane:Plane):
    try:
        query = """
        INSERT INTO planes (Make, Model, Capacity, Age) VALUES (?, ?, ?, ?)
        """

        with closing(conn.cursor()) as c:
            c.execute(query, (plane.make, plane.model, plane.capacity, plane.age))
            conn.commit()

    except sqlite3.OperationalError:
        print("Failed to save plane")


def save_passenger(passenger:Passenger):
    try:
        query = """
        INSERT INTO passengers (FirstName, LastName, PhoneNumber, Email, Address) VALUES (?, ?, ?, ?, ?)
        """

        with closing(conn.cursor()) as c:
            c.execute(query, (passenger.first_name, passenger.last_name, passenger.phone, passenger.email, passenger.address))
            conn.commit()

    except sqlite3.OperationalError:
        print("Falied to save passenger")


def save_flight(flight:Flight):
    try:
        query = """
        INSERT INTO flights (PlaneID, STD, STA, Origin, Destination, MilesTravelled) VALUES (?, ?, ?, ?, ?, ?)
        """

        with closing(conn.cursor()) as c:
            c.execute(query, (flight.plane.id, flight.start_time, flight.arrival_time, flight.origin, flight.destination, flight.miles_travelled))
            conn.commit()

    except sqlite3.OperationalError:
        print("Failed to save flight")


def assign_passanger(passenger_id, flight_id):
    try:
        query = """
        INSERT INTO passengerToFlights (PassengerID, FlightID) VALUES (?, ?)
        """

        with closing(conn.cursor()) as c:
            c.execute(query, (passenger_id, flight_id))
            conn.commit()

    except sqlite3.OperationalError:
        print("Failed to assign passenger to flight")