relation model Re_model01

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

R2(_d1:Real, db)
    constraints
        dom(d2)=Real

relation R3
    | documentation
    columns
        _a : String
        _b : Integer
        c : Integer
        d : Real
    constraints
        key a,b
        key b,c
        a,b -> c,d
        b,c -> a,d
        c -> d
        R1[d] <= R2[d1]
    transformation
        | this is the explaination of the
        | transformation
        rule R1
        rule R2
        concepts
            A
            B.c


relation R4(a,b,c)

