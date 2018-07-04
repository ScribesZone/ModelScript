class model Cl_main_CyberCompany_b
    # include some inheritance (Manager)
    # include association class (Control with frequence)

class Employee
    attributes
        name : String
        age : Integer
        salary : Real
    # operations
    #    raiseSalary(amount : Real) : Real

class Manager < Employee
    attributes
        office : Integer

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
        department : Department[1..*]

association WorksOn
    roles
        employees : Employee[*]
        projects : Project[*]

# association class Control
#    roles
#        department : Department[1]
#        project : Project[*]
#    attributes
#        frequence : Integer


# constraints: see use ocl example

