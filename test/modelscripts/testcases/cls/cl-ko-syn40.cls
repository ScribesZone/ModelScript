    #@Issue cl.syn.Cardinality.Error 1
    #@Issue else *

class model Simple

class Bar

association Foo
    roles
        role1 : Bar[-1..1]
        role2 : Bar[*]

