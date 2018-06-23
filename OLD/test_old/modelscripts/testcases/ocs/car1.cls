class model car1
--@ import constraint model from "car-car-1.ocs"
--@ import constraint model from "car-person-2.ocs"

class Car
attributes
    length : Integer
    width : Integer
end

class Person
attributes
    name : String
    loveCars : Boolean
end

association Owns
between
    Person[0..1] role owner
    Car[*] role cars
end

