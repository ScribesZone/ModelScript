

# TODO:2 handle 'Nothing to do, because file' in merge
#       check with us01scs  without ?0
#       currently the merger generate an empty file
#
# glm gld glossary model
# ucm ucd usecase model
# clm cld class model
# obm obd object model
# scm     scenario model
# pmm     permission model
# acm     access model
#
#
#
#
# ucm  -s e     system actor usecase
# clm  -s e     enumeration class attribute operation association role inv
# obm  -s e  -- clm   object link objectlink
# scm  -s e  -- ucm clm     actori block operation assertion
# pmm  -s e  -- ucm clm
#
#

#
#
#
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
