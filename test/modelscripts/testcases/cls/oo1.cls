model OO1

class C
attributes
    a : Integer
operations
    getA() : Integer
        begin
        result := self.a
        end
    setA(a:Integer)
        begin
        self.a := a
        end
end