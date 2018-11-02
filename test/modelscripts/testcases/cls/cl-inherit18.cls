    //@Issue cl.fin.Cycle.One 2
    //@Issue cl.fin.Cycle.Final 1
    //@Issue else *

class model Cl_intherit_01


class BigThing < Thing

class Animal < Thing

class Elephant < BigThing, Animal, Thing

class Object < Thing

class Thing < Object