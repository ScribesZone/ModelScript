# coding=utf-8

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
# TODO:1 add tags {a,b,c=t} -> -- @a @b @c=t
#       add parsing on the parser side + metamodel
# TODO:1 add {id} semantics -> generation of ocl
#        constratint C.x{id} C.y{id]
#        ->  constraint inv none:C: C.allInstance->isUnique(c|Tuple{c.x,c.y})
# TODO:1 add constraint composition[0..1,1]
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

# TODO:2 full support for frozen, readOnly
# TODO:1 what to do with unique nonUnique orderted
# TODO:1  relational class model  checks
# - pas d'association n-n
# - pas de classes associatives
# - pas de composition avec 0..1 du coté du composite
# - pas d'aggregation
# - pas de generalisation
# - pas de classe abstraite
# TODO:1 support for rôle / × > addonly
# TODO:1 enable glossary in all models
# TODO:1 add inheritance in cl metamodel
# TODO:1
# FIXME:1 display /tmp error in sex/use
#        for metamodels, since composed metamodels are
#        important (e.g. permissoion -> usecase)
# TODO:1 add @assertion in .ob .sc
# TODO:1 import between cl diagram could be very useful
# TODO:2 add syntax enumeration x ... end
#        easy for first and other lines, but must have context for "end"
# TODO:2 Installation procedure.
#       chmod +x for internal model-use
#       chmox +x for bin/*
#
# TODO:2 add [0..1] constraint   not self.x->isUndefined
#
# TODO:3 disable x : Class where Class si not datatype
# TODO:2 datatype Date < String
#       this just replace x : Date by x : String
#       to simplify no "end" keyword
#       other datatype are in fact not really useful
#       since their creation is not easy
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
