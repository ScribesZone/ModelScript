class model Cl_package01

class Elephant
enumeration Before
    foo

datatype Before2

package a

enumeration After
    bar

datatype After2

class Banana
class Tree

association Eat
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

association Contains
    roles
        tree : Tree[1]
        bananas : Banana[*]