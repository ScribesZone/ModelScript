class model Employee
    | This model describes how a company employs employee
    | and generate money through the use of project.

class Person
    | This class is used to represents all people known in
    | the context of the system and not all people in the world.
attributes
    name : String
        | The name of a person stores in fact its firstname and
        | then its family name in upper cases.
    age : Integer
        | The age of the person as far as we know.
        | This value is incremented each year.
    salary : Real
        | The current salary of the person in the current company.
operations
    raiseSalary(rate : Real) : Real
        | The salary of an employe can be raised with a given
        | percentage. 'rate' is the percentage represented using
        | a real number between 0 and 1.
end
| test
class Company
    | Company in the interest.
attributes
  name : String
    | The name of the company in uppercases.
  location : String
operations
  hire(p : Person)
    | Hire the person 'p' making he or she employee of the company/
  fire(p : Person)
    | Fire the person 'p'
end

-- associations

association WorksFor
    | An person can work for at most one company.
between
    Person[*] role employees
        | The employees working in a given company
    Company[0..1] role employer
        | The company that employs the employees.
end

-- constraints

constraints

context self:Person
    inv salaryPositive:
        | The salary of an employee is greater than 0
        self.salary > 0

context Person::raiseSalary(rate : Real) : Real
    post raiseSalaryPost:
        | The salary is increased according to the rate.
        salary = salary@pre * (1.0 + rate)
    post resultPost:
        | The operation return the new salary of the person
        result = salary

context Company::hire(p : Person)
    pre  hirePre1: p.isDefined()
        | The parameter is defined
    pre  hirePre2: employees->excludes(p)
        | The person is not already an employee of the company
    post hirePost: employees->includes(p)
        | The person is employed by the company

context Company::fire(p : Person)
    pre  firePre:  employees->includes(p)
    post firePost: employees->excludes(p)

