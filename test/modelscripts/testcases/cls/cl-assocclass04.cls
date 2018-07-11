class model Cl_association01

class Elephant
class Banana
class Tree

class NiceThing
class TimeSlice

abstract association class Meal < NiceThing, TimeSlice
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

