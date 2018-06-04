class model CyberCompany

class Employee
    attributes
        name : String
        salary : Integer

class Manager extends Employee

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

