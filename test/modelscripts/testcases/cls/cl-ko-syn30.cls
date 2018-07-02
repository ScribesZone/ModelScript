    #@Issue cl.syn.Role.Defined 1
    #@Issue else *

class model Simple

class Bar

association Foo
    roles
        bar : Bar[1]
        bar : Bar[*]

