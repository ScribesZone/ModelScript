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

R2(_d1:Real, dba)
    constraints
        dom(d2)=Real

relation R3(_a,_b,c,d,e,f,g)
    | documentation
    columns
        #TODO: _ a : String
        #TODO: #a : String
        _b : Integer
        c : Integer?
        d : Real
        e : {1,3,2}
        f : {"a", 'b', "e"}
        g : {12.3, 1.5} ?
    constraints
        key a,b
        key b,c
        # TODO prime a
        # TODO prime b
        # TODO non prime f
        a,b -> c,d
        b,c -> a,d
        # TODO a /> c
        # TODO ffd c -> d
        # TODO non ffd z->e
        # TODO 1NF, 2NF, 3NF, BCNF, 4NF
        # TODO {a}+ = {a,b,c}
        R1[d] <= R2[d1]
    #TODO: dependencies + idem
    #TODO: form: 1NF, 2NF, ...
    transformation
        | this is the explaination of the
        | transformation
        rule R1
        rule R2
        concepts
            A
            B.c


relation R4(a,b,c)

