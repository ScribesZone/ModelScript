    #@Issue txt.TermNotFound 2
    #@Issue else *

class model C
import glossary model from 'g01.gls'

class Personne

association EstParentDe
    roles
        parents : Personne[*]
            | `Un` chiffre sur `Deux`
            | and various lines
            | and with `Nothing`
        enfants : Personne[0..2]
            | `Un` chiffre sur `Deux`
            | and various lines
            | and with `Nothing`
