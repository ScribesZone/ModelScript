class model Cl_package01

package a
class Elephant

class Banana
class Tree

association Eat
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

composition Contains
    roles
        tree : Tree[1]
        bananas : Banana[*]