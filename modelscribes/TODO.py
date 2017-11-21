# coding=utf-8

# TODO:0 improve modelc with option
#       (use cli + config)
# TODO:0 error not always printed !
#        printer must inherit message printing from
# TODO:0 bind object/evaluation model issuebox with scenario
#        otherwise there is no error reported when building objects
# TODO:0 chech error/print for main language
# TODO:0 handle use message 'Nothing to do, because file' in merge
#       check with us01scs  without ?0
#       currently the merger generate an empty file
#       is should be enough to first check soil line
#       if not, just compile /use if imported
#       otherwise just print comments
# TODO:0 add constraint composition[0..1,1]
# TODO:1 add Date type -> Integer (20171205)
# TODO:1 add / for derived attributes
# TODO:1 add sex parser to support composition
# (ScribesEnv)jmfavre@jmfavre-HP-ZBook-15:/D2/ScribesZone/ModelScribes/test/modelscripts/testcases/sex$ use -qv composition.use composition3.soil
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# checking structure...
# Error: Object `Wheel1' is shared by object `Car1' and object `Car3'.
# Multiplicity constraint violation in association `HasWheel':
#   Object `Wheel1' of class `Wheel' is connected to 3 objects of class `Car'
#   at association end `car' but the multiplicity is specified as `1'.
# checked structure in 1ms.
# checking invariants...
# checked 0 invariants in 0.000s, 0 failures.



# TODO:1 enable glossary in all models
# TODO:1 add inheritance in cl metamodel
# FIXME:1 display /tmp error in sex/use
#        for metamodels, since composed metamodels are
#        important (e.g. permissoion -> usecase
# TODO:1 add @assertion
# TODO:1 import between cl diagram could be very useful
# TODO:1 add check attribute 0..1

#
# TODO:3 disable x : Class in use
# TODO:2 enable 0package
# TODO:2 check permission analysis
# TODO:3 re parser
# TODO:3 is parser
# TODO:3 oc parser -> cl


#TODO: improve error management

#TODO: add options to bin/modelc.py (-p, -s, ...)
#TODO: check association/class metamodel

#TODO: check what to do with  (link)object destruction

#TODO: check plantuml generation

#TODO: add support for @assert inv / query
#TODO: add support for 'include x.obm' in scenarios

# #TODO: plantuml, check how to get errors from generation

# megamodels
# ----------
# * parser
# * summary/metrics
#
# glossaries
# ----------
#
# * metamodel
# * parser
# * integration in other models
# * summary/metrics
#
# usecases
# --------
#
# * summary
# * error checking
# * printer
# * add management of description
# * priority, interface, etc.
# * scm coverage - scm
# * pmm/clm coverage -- pmm ucm
#
# classes
# -------
#
# * refactor associationClass
# * add package statement
# * spec for clm language ?
# * check a few things in the parser
# * check if comment handling is ok
# * add a few test to check result
# * coverage of invariant wrt class model
# * pmm/ucm coverage -- pmm ucm
#
# objects
# -------
#
# * summary/metrics
# * add description
# * add the possibility to include other obm files at the begining
#   (avoid circular dependencies)
# * clm coverage
#
# scenarios
# ---------
#
# * summary/metrics
# * generation of access model
# * add the possibility to include a obm
# * add description
# * spec for scm as own language (while based on soil)
# * implement assertions (inv + query)
# * ucm coverage
# * clm coverage
# * plm coverage
#
# permissions
# -----------
#
# * summary/metrics?
# * improve language
# * pmm/
#
# access
# ------
#
# * define objectives
# * define language
#
