class model Cl_main_CyberCompany_10

class Department

class Project

association class Control
    roles
        department : Department[1]
        projects : Project[*]
    attributes
        frequency : Integer
