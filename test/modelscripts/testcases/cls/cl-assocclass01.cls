    //@Metric "package" 1
    //@Metric "data type" 8
    //@Metric "enumeration" 0
    //@Metric "enumeration literal" 0
    //@Metric "class" 4
    //@Metric "plain class" 3
    //@Metric "association" 1
    //@Metric "plain association" 0
    //@Metric "association class" 1
    //@Metric "role" 2

class model Cl_association01

class Elephant
class Banana
class Tree

association class Meal
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

