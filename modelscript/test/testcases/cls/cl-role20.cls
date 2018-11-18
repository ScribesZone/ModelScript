class model Cl_association01

class Elephant
class Banana
class Tree

association Contains1
    roles
        tree : Tree[1]
        bananas : Banana[*]

association Contains2
    roles
        x tree : Tree[1]
        > bananas : Banana[*]

association Contains3
    roles
        > tree : Tree[1]
        x bananas : Banana[*]

association Contains4
    roles
        x tree : Tree[1]
        x bananas : Banana[*]

association Contains5
    roles
        > tree : Tree[1]
        > bananas : Banana[*]

association Contains6
    roles
        > tree : Tree[1]
        bananas : Banana[*]

association Contains7
    roles
        > tree : Tree[1]
        bananas : Banana[*]