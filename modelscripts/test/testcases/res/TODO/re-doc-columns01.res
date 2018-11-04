// fillModel should be implemented in order to have this
// the detection of TermNotFound. This relies on
// the creation of text models.

    //@Issue txt.TermNotFound 2
    //@Issue else *

relation model M
import glossary model from 'g01.gls'

relation R
    columns
        t : String
        c : Integer
        d : Real
            | `Un` chiffre sur `Deux`
            | and various lines
            | and with `Nothing`