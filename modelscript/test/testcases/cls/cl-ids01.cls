class model Cl_uds01


// No id -> no errors
class Food
    attributes
        yummy : Boolean
        name : String

class Employee
    attributes
        firstName : String {id}
        lastName : String {id}
        age : Integer {id}
        country : String

// All attributes ids
class Country
    attributes
        name : String {id}

// All attributes ids
class Number
    attributes
        name : String {id}
        value : Integer {id}

