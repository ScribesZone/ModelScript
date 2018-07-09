class model Cl_uds01

class Employee
    attributes
        firstName : String {id}
        lastName : String {id}
        age : Integer {id}
        country : String


class Country
    attributes
        name : String {id}

class Food
    attributes
        yummy : Boolean
        name : String

