    // Cycle in inheritance relationships

        //@Metric "plain class" 6
        //@Metric "class" 6
        //@Metric "association class" 0
    //@Issue cl.syn.Class.NoSuper 2
    //@Issue level *

class model Cl_class01

class A < A

class B < C

class C < B

class D < C

class F < D

class G < A, B, C