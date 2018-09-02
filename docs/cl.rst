.. .. coding=utf-8

cl - CLass models
=================

Examples
--------

::

    class model
        | This model describes


    enum MyEnum:
        | comment for the enum
        a
            | text for this value
        b
        v


    abstract class A < B:
        { abstract }
        | The site could be temporarily unavailable or too busy.
        | Try again in a few moments. If you are unable to load any
        | pages, check your computer’s network connection.
        | If your computer or network is protected by a firewall
        | or proxy, make sure that Firefox is permitted to access the
        | Web.
        attributes:
            "init" x : String {unique} {id}
                {x=3}
                | The site could be temporarily unavailable or too busy.
                | Try again in a few moments. If you are unable to
                | load any check your computer’s network connection.
                permissions:
                    Employee, Student can R
                    Prendre can RU
            r : Integer[0..1]

            hasItems : Boolean

            /isBlocked : Boolean
                def: Z

        operations:
            op(p1:X):Set(X):
                | The site could be temporarily unavailable or too busy.
                def: x+3*6*(
                    +c)
                pre a1:
                    True
                post a2:

            op2
        invariants
            inv1 :
                true
        permissions:
            actor Employee : CRUD
            actor Student : R
            usecase RetirerA : CUD

    association X:
        roles:
            A : B[*]
            B : A[0..1]

    associationclass R < C:
        roles:
            A : B[*]
            B : A[0..1]
        attributes:
            x : String
            c : Photo
        operations:
            op()
            op2


    invariant A:
        | a
        location:
        python:
            dfjgldskfsgjdlfg
        ocl:
            True and
            False

Classes
-------

Associations
------------

Invariants
----------
