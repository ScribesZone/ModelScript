    # Cycle in inheritance relationships

    #@Metric "plain class" 6
    #@Metric "class" 6
    #@Metric "association class" 0
    #@Issue cl.syn.Class.NoSuper 2
    #@Issue level *

class model Cl_class01

class A extends A

class B extends C

class C extends B

class D extends C

class F extends D

class G extends A, B, C