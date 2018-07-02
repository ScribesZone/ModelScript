    #@Issue cl.syn.GlobalName.Twice 1
    #@Issue else *


class model Simple

class Again

association Again
    roles
        xyz : Again[0..1]
        ztr : Again[*]



