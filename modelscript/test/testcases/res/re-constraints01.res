relation model M

relation R1
    columns
        a
        b
        c
        d
    constraints
        dom(a)=String
        dom(b)=dom(c)=String
        key a,b
        key b,c
        a,b -> c,d
        b,c -> a,d
        c -> d

relation R2
    columns
        x
        y : String
    constraints
        R2[y] C= R1[a]
