class model Cl_main_CyberCompany_a

class Employee
    attributes
        name : String
        salary : Integer

class Department
    attributes
        name : String
        location : String
        budget : Integer

class Project
    attributes
        name : String
        budget : Integer

association WorksIn
    roles
        employees : Employee[*]
        departments : Department[1..*]

association Controls
    roles
        department : Department[1]
        projects : Project[*]

association WorksOn
    roles
        employees : Employee[*]
        projects : Project[*]

association Supervise
    roles
        supervisor : Employee[1]
        subordinates : Employee[*]

invariant salaryPositive
    | This is a test
    scope
        derive A
        B.B
        C


