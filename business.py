class Passenger():
    id:int = 0
    first_name:str
    last_name:str
    phone:str
    email:str
    address:str

class Plane():
    id:int = 0
    make:str
    model:str
    capacity:int
    age:int

class Flight():
    def __init__(self):
        self.id:int = 0
        self.plane:Plane
        self.passengers:list[Passenger] = []
        self.start_time:str
        self.arrival_time:str
        self.origin:str
        self.destination:str
        self.miles_travelled:int

    def has_open_seats(self):
        if self.plane.capacity > len(self.passengers):
            return True
        return False

    def add_passenger(self, passenger):
        if self.has_open_seats():
            self.passengers.append(passenger)
        else:
            return None