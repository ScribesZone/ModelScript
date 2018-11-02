    // misc: operation, local invariants, permissions

class model Cl_main
    | this is the documentation of the class

class Empty
    | This class is empty

class C
    | this is a doc line for the class ; .
    | with two lines
    attributes
        x : Integer
            | documenation of attribute x
        y : Real
    operations
        f() :   Integer
            | documentation of operation f
        g()
    invariants
    permissions

class D < C
    attributes

enumeration A
    | this is the documentation of the enumeration
    x
    y
    z
enumeration B
    t
    u

association
    roles
        cs : C
        d : D

invariant
