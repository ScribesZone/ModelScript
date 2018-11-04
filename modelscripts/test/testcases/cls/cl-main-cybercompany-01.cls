class model Cl_main_CyberCompany_01

class Employee

class Department


association WorksIn
    roles
        employees : Employee[*]
        departments : Department[1..*]
