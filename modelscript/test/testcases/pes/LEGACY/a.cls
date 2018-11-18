class model A

class C
attributes
    cs : String
    ci : Integer
end

class D
attributes
    ds : String
end

association R between
    C[*] role r1
    D[*] role r2
end

associationclass S between
    C[1] role s1
    D[1] role s2
attributes
    sa : String
end