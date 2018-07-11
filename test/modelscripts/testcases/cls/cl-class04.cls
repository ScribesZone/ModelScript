    #@Metric "plain class" 3
    #@Metric "class" 3
    #@Metric "association class" 0
    #@Issue cl.res.Class.NoSuper 2
    #@Issue level *

class model Cl_class01

abstract class A < Nothing

class B < A

class C < B, Nothing, A