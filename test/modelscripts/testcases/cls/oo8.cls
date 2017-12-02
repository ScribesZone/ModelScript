model OO8

class Car
attributes
    owner : Person
operations
    _setOwner(o:Person)
        begin
        self.owner := o
        end
    setOwner(o:Person)
        begin
        o.addCar(self)
        end
end

class Person
attributes
    cars : Set(Car) init: Set{}
operations
    addCar(c:Car)
        begin
        self.cars:=self.cars->including(c) ;
        c._setOwner(self)
        end
end


constraints

context self : Car
inv inverseOwnerCars:
    self.owner.cars->includes(self)