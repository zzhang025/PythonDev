# imports


# Vehicle class
class Vehicle:
    def __init__(self, license, spot_size):
        self._license = license
        self._spot_size = spot_size

    def get_spot_size(self):
        return self._spot_size

    def get_license(self):
        return self._license


class Driver:
    def __init__(self, id, vehicle):
        self._id = id
        self._vehicle = vehicle
        self._payment_due = 0

    def get_vehicle(self):
        return self._vehicle

    def get_id(self):
        return self._id

    def charge(self, amount):
        self._payment_due += amount


class Car(Vehicle):
    def __init__(self, license):
        super().__init__(license, 1)


class Limo(Vehicle):
    def __init__(self, license):
        super().__init__(license, 2)


class SemiTruck(Vehicle):
    def __init__(self, license):
        super().__init__(license, 3)


class ParkingFloor:
    def __init__(self, spot_count):
        self._spots = [0] * spot_count  # 0 means empty, 1 means occupied
        self._vehicle_map = {}  # maps vehicle to spot index

    def park_vehicle(self, vehicle):
        size = vehicle.get_spot_size()
        l, r = 0, 0
        while r < len(self._spots):
            if self._spots[r] != 0:
                l = r + 1
            if r - l + 1 == size:  # found a spot
                for k in range(l, r + 1):
                    self._spots[k] = 1
                    self._vehicle_map[vehicle.get_license()] = (l, r)
                return True
            r += 1
        return False

    def remove_vehicle(self, vehicle):
        start, end = self._vehicle_map[vehicle.get_license()]
        for i in range(start, end + 1):
            self._spots[i] = 0
        del self._vehicle_map[vehicle.get_license()]

    def get_parking_spots(self):
        return self._spots

    def get_vehicle_sports(self, vehicle):
        return self._vehicle_map[vehicle.get_license()]

class ParkingGarage:
    def __init__(self, floor_count, spots_per_floor):
        self._parking_floors = [ParkingFloor(spots_per_floor) for _ in range(floor_count)]

    def park_vehicle(self, vehicle):
        for floor in self._parking_floors:
            if floor.park_vehicle(vehicle):
                return True       
        return False
    
    def remove_vehicle(self, vehicle):
        for floor in self._parking_floors:
            if vehicle.get_license() in floor._vehicle_map:
                floor.remove_vehicle(vehicle)
                return True
        return False

import datetime 
import math 

class ParkingSystem:
    def __init__(self, parking_garage, hourlyRate):
        self._parking_garage = parking_garage
        self._hourlyRate = hourlyRate
        self._timeParked = {}

    def park_vehicle(self, driver):
        currentHour = datetime.datetime.now().hour
        isParked = self._parking_garage.park_vehicle(driver.get_vehicle())
        if isParked:
            self._timeParked[driver.get_id()] = currentHour

        return isParked
    
    def remove_vehicle(self, driver):
        if driver.get_id() not in self._timeParked:
            return False
        currentHour = datetime.datetime.now().hour
        timeParked  = math.ceil(currentHour - self._timeParked[driver.get_id()])
        driver.charge(timeParked * self._hourlyRate)

        del self._timeParked[driver.get_id()]
        return self._parking_garage.remove_vehicle(driver.get_vehicle())
        
parkingGarage = ParkingGarage(3, 2)
parkingSystem = ParkingSystem(parkingGarage, 5)

driver1 = Driver(1, Car("123C"))
driver2 = Driver(2, Limo("456L"))
driver3 = Driver(3, SemiTruck("789S"))

print(parkingSystem.park_vehicle(driver1))      # true
print(parkingSystem.park_vehicle(driver2))      # true
print(parkingSystem.park_vehicle(driver3))      # false

print(parkingSystem.remove_vehicle(driver1))    # true
print(parkingSystem.remove_vehicle(driver2))    # true
print(parkingSystem.remove_vehicle(driver3))    # false