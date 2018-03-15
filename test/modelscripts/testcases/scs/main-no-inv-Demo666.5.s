USE version 4.2.0, Copyright (C) 1999-2016 University of Bremen
java.lang.UnsatisfiedLinkError: no natGNUReadline in java.library.path
Apparently, the GNU readline library is not available on your system.
The program will continue using a simple readline implementation.
You can turn off this warning message by using the switch -nr
Demo666.5.soil> ! x := new Employee('sophie')
Demo666.5.soil> check -v -d -a
checking structure...
Multiplicity constraint violation in association `WorksIn':
  Object `sophie' of class `Employee' is connected to 0 objects of class `Department'
  at association end `department' but the multiplicity is specified as `1..*'.
checked structure in 5ms.
checking invariants...
checked 0 invariants in 0.000s, 0 failures.
Demo666.5.soil> ! x := new Employee('mario')
Demo666.5.soil> check -d -a
checking structure...
Multiplicity constraint violation in association `WorksIn':
  Object `mario' of class `Employee' is connected to 0 objects of class `Department'
  at association end `department' but the multiplicity is specified as `1..*'.
Multiplicity constraint violation in association `WorksIn':
  Object `sophie' of class `Employee' is connected to 0 objects of class `Department'
  at association end `department' but the multiplicity is specified as `1..*'.
checked structure in 9ms.
checking invariants...
checked 0 invariants in 0.001s, 0 failures.
Demo666.5.soil> 
use> use> 