scenario model


-- @assert Department::MoreEmployeesThanProjects OK
-- @assert Employee::MoreProjectsHigherSalary OK
-- @assert Project::BudgetWithinDepartmentBudget OK
-- @assert Project::EmployeesInControllingDepartment OK

-- checking structure...
-- checking invariants...
-- checking invariant (1) `Department::MoreEmployeesThanProjects': OK.
-- checking invariant (2) `Employee::MoreProjectsHigherSalary': OK.
-- checking invariant (3) `Project::BudgetWithinDepartmentBudget': OK.
checking invariant (4) `Project::EmployeesInControllingDepartment': OK.

The site could be temporarily unavailable or too busy. Try again in
a few moments. If you are unable to load any pages, check your
computer’s network connection. If your computer or network is
protected by a firewall or proxy, make sure that Firefox is permitte
to access the Web.
    !create computing : Department
    !computing.name := 'Computing departement'
    !computing.location := 'Los alaambritos'
    !computing.budget := 10000

The site could be temporarily unavailable or too busy.

    !create djamel : Employee
    !djamel.name := 'Djamel'
    !djamel.salary := 2600

If you are unable to load any pages, check your computer’s network connection. If your computer or network is

    !create ioannis : Employee
    !ioannis.name := 'Ioannis'
    !ioannis.salary := 1900

protected by a firewall or proxy, make sure that Firefox is permitte
to access the Web.



    !insert (djamel, computing) into WorksIn
    !insert (ioannis, computing) into WorksIn

    !create turbo : Project
    !turbo.name := 'Maxi turbo project'
    !turbo.budget := 5000

    !insert (computing, turbo) into Controls
