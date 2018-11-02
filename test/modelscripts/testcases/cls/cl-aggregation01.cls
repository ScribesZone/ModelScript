        //@Issue cl.syn.Association.NotAggreg 1
        //@Issue else *

class model Cl_association01

class Elephant
class Banana
class Tree

aggregation Meal
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

