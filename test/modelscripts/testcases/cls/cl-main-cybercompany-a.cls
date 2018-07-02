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
        departments : Department[0..*]

association Controls
    roles
        department : Department[*]
        projects : Project[*]

association WorksOn
    roles
        employees : Employee[*]
        projects : Project[*]

association Supervise
    roles
        supervisor : Employee[*]
        subordinates : Employee[*]
