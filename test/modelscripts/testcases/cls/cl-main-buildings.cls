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


//=======================================================================
//                        constraints
//=======================================================================


invariant floorOrder
    | The maximum floor is higher or at the same level
    | that the minimum floor of the residence.
    scope
        Residence.floorMin
        Residence.floorMax
    ocl
        context self : Residence
        self.floorMin <= self.floorMax

invariant floorBetweenMinAndMax
    | Floor between minimum and maximum floors.
    | The floor of a room is between the minimum and maximum
    | floor of the residence.
    ocl
        context self : Room
        self.floor >= self.residence.floorMin
        and self.floor <= self.residence.floorMax

invariant deriveFloor
    | Derivation of the attribute floor.
    | The floor number correspond to the first digits of the room
    | number, where the last two digits are removed.
    | For instance the room 634 is at the floor 6.
    ocl
        context self : Room
        floor = number div 100

invariant deriveIsOnTheLanding
    | Derivation of isOnTheLanding attribute.
    scope
        derive isOnTheLanding
        Bedroom.isEmpty
    ocl
        context self : Bathroom
        isOnTheLanding = self.bedroom->isEmpty()

invariant deriveMaxNbOfFreeUnits
    | The maximum number of free units is equal to the maximum
    | number of places in beds of all rooms of the residence.
    scope
        derive Residence.maxNbOfFreeUnits
    ocl
        context self : Residence
        maxNbOfFreeUnits =
            self.rooms->selectByType(Bedroom)
                .nbOfUnits->sum()

invariant deriveAvgRate
    | The average rate of a residence is the total revenue
    | of the residence divided by the number of occupants.
    | Tutored residents do not count in this rule.
    scope
        derive Residence.avgRate
        ContainsRooms
        Rent
        Tenant.paidRate
        IsOccupiedBy
        IsTutoredBy
    ocl
        context self : Residence
        avgRate =
            self.rooms
                ->selectByType(Bedroom)
                .tenant.paidRate
                ->asSet()->sum()
                / (self.rooms->selectByType(Bedroom).occupants
                    ->select(tutors->isEmpty())->size())

invariant uniqueNumberApartForPrivateBathroom
    | Invariant on room numbering.
    | All rooms have a distinct number, except private bathrooms.
    scope
        Room.number
        ContainsRooms
        IsInBedroom
    ocl
        context self : Residence
        (self.rooms - (self.rooms->selectByType(Bathroom)
            ->select(isOnTheLanding)))
                -> isUnique(number)

invariant allPrestigeBathrooms
    | Invariant about all bathrooms for 'prestige' residence.
    | Residences of category prestige have in each bedroom
    | at least the same number of bathroom that the number of beds.
    scope
    ocl
        context self : Residence
        self.category = #prestige implies
            self.rooms->selectByType(Bedroom)->forAll(
                bathrooms->size() >= nbOfSingleBeds+nbOfDoubleBeds)
















//
//
//-- Same number if private.
//-- Easy. Use 'implies'.
//context self : Bathroom inv sameNumberIfPrivate :
//    -- All bathrooms that are not on the landing, that is that are private to a bedroom, have the same number of room as this bedroom.
//    not self.isOnTheLanding implies
//    self.number = self.bedroom.number
//
//-- Out of order bathroom implications if prestige.
//-- Medium. Use 'implies'
//context self : Bathroom inv oooIfPrestige :
//    -- In prestige residences, it is not acceptable to rent bedrooms with bathrooms that are out of order. So if a bathroom is marked as out of order, the corresponding bedroom is also marked as out of order.
//    (       self.residence.category = #prestige
//    and  self.isOutOfOrder
//    and  self.bedroom->notEmpty())
//          implies
//                self.bedroom.isOutOfOrder
//
//-- At least one bed for useful bedrooms.
//-- Easy. Use implies.
//context self : Bedroom inv atLeastABed :
//    -- Bedrooms that are not out of order must have at least one bed.
//    not self.isOutOfOrder implies
//        self.nbOfSingleBeds + self.nbOfDoubleBeds >= 1
//
//-- At least as many bathrooms than beds for prestige residence.
//-- Easy. Use implies.
//context self : Bedroom inv enoughBathroomsInPrestige :
//    -- In a prestige residence, the number of private bathrooms is at least the same as the number of beds in each bedroom.
//    self.residence.category = #prestige implies
//        self.bathrooms->size() >= self.nbOfSingleBeds+self.nbOfDoubleBeds
//
//-- Derivation of nbOfUnits attribute.
//-- Easy
//context self : Bedroom inv deriveNbOfUnits :
//    -- The number of units of a bedroom is the maximum number of people that can fit within the bedroom assuming that all places in all beds are full.
//    nbOfUnits = self.nbOfSingleBeds + 2*self.nbOfDoubleBeds

//-- No smoking is prestige.
//-- Easy
//context self : Bedroom inv smokingPrestigePolicy :
//    -- There are no smoking rooms at all in residence of prestige.
//    self.residence.category = #prestige implies
//        self.isNonSmoking



//---------------------------------------------------------------------
//-- Rented bedrooms not empty.
//-- Easy. Use 'implies'
//context self : Bedroom inv noEmptyRentedBedrooms :
//    -- All rented bedrooms are occupied by at least one occupant.
//    self.tenant->notEmpty() implies self.occupants->notEmpty()
//
//-- At least one adult per room.
//-- Easy. Use 'implies'
//context self : Bedroom inv atLeastOneAdult :
//    -- At least one adult must be presented in all occupied rooms.
//    self.occupants->notEmpty() implies
//        self.occupants->exists(age>=18)
//
//-- Nobody in rooms not rented.
//-- Easy. Use 'implies'
//context self : Bedroom inv noSquaters :
//    -- Occupants must be exclusively in rooms that are rented by somebody.
//    self.tenant->isEmpty() implies
//        self.occupants->isEmpty()
//
//-- No bedroom overloaded.
//-- Medium
//context self : Bedroom inv noBedroomOverload :
//    -- There must be no more people in a bedroom that the number of units of this bedroom. Children up to 3 years old are not counted in this rule.
//    self.occupants->select(age>3)
//        ->size() <= self.nbOfUnits
//
//-- No rental of Out Of Order bedrooms.
//-- Easy
//context self : Bedroom inv oooBedroomsNotRented :
//    -- Bedrooms that are out of order cannot be rented.
//    self.isOutOfOrder implies self.tenant->isEmpty()
//
