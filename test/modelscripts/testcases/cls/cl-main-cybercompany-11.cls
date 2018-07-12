class model Cl_main_CyberCompany_10

class Department
    attributes
        name : String
        location : String
        budget : Integer

class Project
    attributes
        name : String
        budget : Integer

association class Control
    roles
        department : Department[1]
        projects : Department[*]
    attributes
        frequency : Integer
