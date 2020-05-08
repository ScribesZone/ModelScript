    // Cycles in inheritance relationships

    //@Metric "plain class" 6
    //@Metric "class" 6
    //@Metric "association class" 0

    //@Issue cl.fin.Cycle.One 5
    //@Issue cl.fin.Cycle.Final 1
    //@Issue else *

class model Cl_class01

class A < A

class B < C

class C < B

class D < C, F

class F < D, F

class G < A, B, C
