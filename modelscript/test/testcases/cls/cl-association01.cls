class model Cl_association01

class Elephant
class Banana
class Tree

association Meal
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]
