    //@Issue cl.fin.Attribute.InhHorizontal 1
    //@Issue else *

class model Cl_inhatt


class BigThing
    attributes
        width : Real
        weight : Integer

class Animal
    attributes
        depth : Real
        weight : Integer
        
class Elephant < Animal, BigThing
    attributes
        color : Integer

class SmallElephant < Elephant
    attributes
        age : Integer