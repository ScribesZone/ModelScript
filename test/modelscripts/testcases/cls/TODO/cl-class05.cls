    # Cycle in inheritance relationships

    #@Metric "regular class" 3
    #@Issue cl.syn.Class.NoSuper 2
    #@Issue level *

class model Cl_class01

class A extends A

class B extends C

class C extends B

class D extends C

class F extends D

class G extends A, B, C