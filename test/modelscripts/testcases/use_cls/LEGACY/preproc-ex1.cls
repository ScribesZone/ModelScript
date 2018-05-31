class model Employee

-- datatype Date < Integer --

package x.b

class Person
attributes
    /name : String
    age : Integer[0..1]
    + pub1 : Integer
    +pub2:Integer
    - priv : Integer
    /+salary : Real[0..1]
    birthdate: String {id} {addOnly, }  --
operations
    raiseSalary(rate : Real) : Real
end
