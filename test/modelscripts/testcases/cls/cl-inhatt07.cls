class model Cl_inhatt


class BigThing
    attributes
        size : Integer

class Animal
    attributes
        weight : Integer
        
class Elephant < Animal, BigThing
    attributes
        color : Integer

class SmallElephant < Elephant
    attributes
        age : Integer