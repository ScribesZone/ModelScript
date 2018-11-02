    //@Issue cl.syn.Association.NoAttribute 1
    //@Issue else *

class model Cl_association01

class Elephant
class Banana
class Tree

association Test
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]
    attributes
        time : Time
