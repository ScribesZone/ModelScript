    #@Issue cl.syn.Role.Defined 1
    #@Issue else *

class model Cl_association01

class Elephant
class Banana
class Tree

class NiceThing
class TimeSlice

association class Meal
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        eater : Banana[*]
