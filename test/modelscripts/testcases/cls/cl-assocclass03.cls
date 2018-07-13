    #@Metric "class" 5
    #@Metric "plain class" 4
    #@Metric "association" 1
    #@Metric "plain association" 0
    #@Metric "association class" 1
    #@Metric "attribute" 0
    #@Metric "role" 2

class model Cl_association01

class Elephant
class Banana
class Tree

class NiceThing

abstract association class Meal < NiceThing
    | Take record of the bananas eaten by elephants.
    roles
        eater : Elephant[0..1]
        bananas : Banana[*]

