    #@Issue cl.syn.GlobalName.Twice 1
    #@Issue else *


class model Simple

class Foo

association Again
    roles
        xyz : Foo[0..1]
        ztr : Foo[*]

association Again
    roles
        xyz : Foo[0..1]
        ztr : Foo[*]

