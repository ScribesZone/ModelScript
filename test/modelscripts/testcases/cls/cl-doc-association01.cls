    #@Issue txt.TermNotFound 1
    #@Issue else *

class model C
import glossary model from 'g01.gls'

class Personne

association EstParentDe
    | `Un` chiffre sur `Deux`
    | and various lines
    | and with `Nothing`
    roles
        parents : Personne[*]
        enfants : Personne[0..2]

