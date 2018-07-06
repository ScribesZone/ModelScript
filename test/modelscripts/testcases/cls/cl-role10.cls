class model Cl_association01

class Elephant
class Banana
class Tree

composition Contains
    roles
        tree : Tree[1] {a, b}
        bananas : Banana[*] << s1, s2 >> {g, e}
