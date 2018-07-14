class model Cl_inhatt


class Thing

class BigThing < Thing
    attributes
        width : Real
        weight : Integer

class Animal < Thing
    attributes
        depth : Real
        weight : Integer
        
class Elephant < Animal, BigThing
