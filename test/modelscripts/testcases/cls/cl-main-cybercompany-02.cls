class model Cl_main_CyberCompany_a

class Employee

class Department

association WorksIn
    roles
        employees : Employee[*]
        departments : Department[*]


association Supervise
    roles
        supervisor : Employee[1]
        subordinates : Employee[*]
