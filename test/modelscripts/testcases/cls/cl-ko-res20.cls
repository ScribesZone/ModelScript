    #@Issue cl.res.Role.NoClass 1
    #@Issue else *

class model Simple

class Employee

association BadThing
    roles
        yes : Employee[1]
        also : Employee[*]

association WorksWithout
    roles
        yes : Employee[*]
        issue : BadThing[*]
