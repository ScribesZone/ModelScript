class model Cl_inhatt


class Thing
    attributes
        name : String

class BigThing < Thing
    attributes
        size : Integer

class Animal < Thing
    attributes
        weight : Integer
        
class Elephant < Animal, BigThing, Thing
    attributes
        color : Integer

class SmallElephant < Elephant
    attributes
        age : Integer