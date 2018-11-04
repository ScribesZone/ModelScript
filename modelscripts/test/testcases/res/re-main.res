relation model Re_model01

R3(_a,_b,c,d)
    1NF
    a,b -> c,d
    c->d
    dom(a)=String
    dom(b)=dom(c)=Integer
    dom(d)=Real?
    R1[d] <= R2[d1]

R1(_a, _b, c, d, e)
    | (a,b,c,d) e R1 <=> Le R dont l'identifiant (a,b) a pour
    | attribute c, d et e.
    constraints
        key a,b
        key b,c
        a,b -> c,d,e
        b,c -> a,d,e
        c -> d
        dom(a)=String
        dom(b)=dom(c)=Integer
        dom(d)=Real?
        R1[d] <= R2[d1]

R2(_d1:Real, dba)
    constraints
        dom(d2)=Real

R2(a,b,c,d)
    | documentation
    key a,b
    key b,c
    a,b -> c,d,e
    b,c -> a,d,e
    c -> d
    dom(a)=String
    dom(b)=dom(c)=Integer
    dom(d)=Real?
    R1[d] <= R2[d1]
    prime a
    prime b
    /prime f
    a -/> c
    c -ffd> d
    z-/ffd>e
    1NF
    2NF
    3NF
    BCNF
    4NF
    {a}+ = {a,b,c}

relation R3(_a,_b,c,d,e,f,g)
    | documentation
    columns
        _ a : String
        #a : String
        _b : Integer
        c : Integer?
        d : Real
        e : {1,3,2}
        f : {"a", 'b', "e"}
        g : {12.3, 1.5} ?
    constraints
        key a,b
        key b,c
        a,b -> c,d
        b,c -> a,d
        R1[d] <= R2[d1]
    properties
        prime a
        prime b
        /prime f
        a -/> c
        c -ffd> d
        z-/ffd>e
        1NF
        2NF
        3NF
        BCNF
        4NF
        {a}+ = {a,b,c}
    transformation
        | this is the explaination of the
        | transformation
        rule R1
        rule R2
        concepts
            A
            B.c


relation R4(a,b,c)

