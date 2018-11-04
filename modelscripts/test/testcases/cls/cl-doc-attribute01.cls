    //@Issue txt.TermNotFound 1
    //@Issue else *

class model C
import glossary model from 'g01.gls'

class Personne
    attributes
        nom : String
            | `Un` chiffre sur `Deux`
            | and various lines
            | and with `Nothing`.
            | This doc should fail.
