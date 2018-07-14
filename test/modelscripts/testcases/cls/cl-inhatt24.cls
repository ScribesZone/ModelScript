
    #@Issue cl.fin.Inheritance.Vertical 4
    #@Issue cl.fin.Inheritance.Horizontal 2
    #@Issue else *

class model Cl_inhatt


class Thing
    attributes
        weight : Integer

class BigThing < Thing
    attributes
        texture : Real
        weight : Integer

class Animal < Thing
    attributes
        depth : Real
        weight : Integer
        
class Elephant < Animal, BigThing

class SmallElephant < Elephant
    attributes
        weight : Integer

class TinyElephant < Elephant, BigThing
    attributes
        color : Integer
        length: Real
        texture : Integer