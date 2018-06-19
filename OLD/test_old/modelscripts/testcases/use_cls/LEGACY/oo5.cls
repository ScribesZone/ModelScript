model OO5

class Car
attributes
    length : Integer
    width : Integer
    owns : Person
end

class Person
attributes
    name : String
    loveCars : Boolean
    cars : Set(Car)
end