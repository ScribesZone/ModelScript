class model Cl_inhatt


class Thing
    attributes
        name : String

class BigThing < Thing
    attributes
        size : Integer

class Animal < Thing
    attributes
        age : Integer
        
class Elephant < Animal, BigThing
    attributes
        color : Integer

class SmallElephant < Elephant
    attributes
        weight : Integer