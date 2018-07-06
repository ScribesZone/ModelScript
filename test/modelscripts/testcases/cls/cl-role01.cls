class model Cl_association01

class Elephant
class Banana
class Tree

composition Contains
    roles
        tree : Tree[1]
        bananas : Banana[*]

composition Contains2
    roles
        x tree : Tree[1]
        > bananas : Banana[*]

composition Contains3
    roles
        > tree : Tree[1]
        x bananas : Banana[*]

composition Contains4
    roles
        x tree : Tree[1]
        x bananas : Banana[*]

association Eat
    | Take record of the bananas eaten by elephants.
    roles
        x eater : Elephant[0..1]
        > bananas : Banana[*]

association Hop
    | Take record of the bananas eaten by elephants.
    roles
        foo : Elephant[0..1]
        > bar : Banana[*]

association Doo
    | Take record of the bananas eaten by elephants.
    roles
        foo : Elephant[0..1]
        x bar : Banana[*]


association None
    | Take record of the bananas eaten by elephants.
    roles
        x foo : Elephant[0..1]
        x bar : Banana[*]

association Both
    | Take record of the bananas eaten by elephants.
    roles
        > foo : Elephant[0..1]
        > bar : Banana[*]

association New
    | Take record of the bananas eaten by elephants.
    roles
        > foo : Elephant[0..1]
        x bar : Banana[*]