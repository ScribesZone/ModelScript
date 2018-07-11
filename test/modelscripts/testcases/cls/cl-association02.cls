    #@Issue cl.syn.Association.NoAbstract 1
    #@Issue else *

class model Cl_association01

class Elephant
class Banana
class Tree

abstract association Test
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]
