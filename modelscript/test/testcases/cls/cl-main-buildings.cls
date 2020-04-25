class model Building

//---------------------------------------------------------------------
package buildings
//---------------------------------------------------------------------

enumeration Category
    economy
    standard
    premium
    prestige

class Residence
    attributes
        name                : String
        description         : String
        floorMin            : Integer
        floorMax            : Integer
        category            : Category
        / maxNbOfFreeUnits  : Integer
        / avgRate           : Real

class Room
    attributes
        number          : Integer
        / floor         : Integer
        isOutOfOrder    : Boolean

class Bathroom < Room
    attributes
        / isOnTheLanding : Boolean

class Bedroom < Room
    attributes
        nbOfSingleBeds  : Integer
        nbOfDoubleBeds  : Integer
        rate            : Real
        isNonSmoking    : Boolean
        / nbOfUnits     : Integer

// TODO: composition ContainsRooms
association ContainsRooms
    roles
        residence : Residence[1]
        rooms : Room[*]

association IsInBedroom
    roles
        bathrooms : Bathroom[0..3]
        bedroom : Bedroom[0..1]


//---------------------------------------------------------------------
package residents
//---------------------------------------------------------------------

enumeration Gender
    male
    female

class Person
    attributes
        name    : String
        age     : Integer
        gender  : Gender

class Resident < Person
    attributes
        isSmoker : Boolean

class Tenant < Resident
    attributes
        paidRate : Real

association IsTutoredBy
    roles
        tutored : Resident[0..*]
        tutors : Resident[0..2]

association IsMarriedWith
    roles
        _consort : Resident[0..1]
        consort : Resident[0..1]

association IsOccupiedBy
    roles
        occupiedRoom : Bedroom[1]
        occupants : Resident[*]

//---------------------------------------------------------------------
package rates
//---------------------------------------------------------------------


class Discount
    attributes
        percentage : Integer
        label : String

association class Rent
    roles
        rentedBedrooms : Bedroom[1..*]
        tenant : Tenant[0..1]
    attributes
        / discount : Real
        / rate     : Real

//TODO: composition HasDiscounts
association HasDiscounts
    roles
        rent : Rent[1]
        discounts : Discount[0..*]

