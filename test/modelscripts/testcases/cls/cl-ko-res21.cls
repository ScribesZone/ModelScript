    #@Issue cl.res.Role.NoClass 1
    #@Issue else *

class model Simple

enumeration BadThing
    y

class Employee

association Department
    roles
        yes : Employee[1]
        issue : BadThing[*]

