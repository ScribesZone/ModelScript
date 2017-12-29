class model Employee

datatype Date < Integer --

package x.b

class Person
attributes
  /name : String -- @Date
  age : Integer[0..1]
  + pub1 : Integer
  +pub2:Integer
  - priv : Integer
  /+salary : Real[0..1]
    birthdate: String {id} {frozen, }  --
operations
  raiseSalary(rate : Real) : Real
end
