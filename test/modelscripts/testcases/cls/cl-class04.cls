    #@Metric "regular class" 3
    #@Issue cl.syn.Class.NoSuper 2
    #@Issue level *

class model Cl_class01

abstract class A extends Nothing

class B extends A

class C extends B, Nothing, A