# class model
#
# #---------------------------------------------
# #
#
#
# Class
# =====
# class <class.name>
# Le concept de <class.name> est important.
# <class.name> is an important concept.
# "File" is an important concept.
# Le concept de "Fichier" est important.
#
# Inheritance
# ===========
# class <a.name> < <class.name>
# A <class.name> is a <class.name>.
# Un|Une <class.name> est un|une <class.name>.
# A "PlainFile" is a "File".
# Un "FichierPlein" est un "Fichier".
#
# Attribute
# =========
# class <class.name>
#     <attribute.name> : <type.name>
# The <attribute.name> of a <class.name> is a <type.name>.
# Le|La|L' <attribute.name> d'un|d'une <class.name> est un|une <type.name>.
# The "size" of a "PlainFile" is an "integer"
# La taille d'un "FichierPlain" est un "entier"
#
# Association
# ===========
#
# association name, role, cardinalite
# -----------------------------------
#
# association <association.name> ...
#     <role1.name> : <class1.name> [role1.card]
#     <role2.name> : <class2.name> [role2.card]
#
# Cardinalities
# '''''''''''''
#
#     [0..*]
#         zero or many
#         zero ou plusieurs
#     [1..*]
#         one or many
#         un|une ou plusieurs
#     [0..1]
#         zero or one
#         zero ou un|une
#     [1..1]
#         one
#         un
#     [x..y]
#         between x and y
#         entre x et y
#
# Structure. Forward direction
# ''''''''''''''''''''''''''''''''''
# A <Class1.name> <association.name> [of] {role2.card} <role2.name> [of] type <Class2.name>.
# Un|Une <Class1.name> <association.name> [de|d'] <role2.card> [de] <role2.name> de type <Class2.name>.
# A "Person" "IsParent" of {zero or many} "children" of type "Person"
# Un "Personne" "EstParent" de {zero ou plusieurs} "enfants" de type of type "Personne".
#
# Structure. Reverse direction
# ''''''''''''''''''''''''''''
# A <Class2.name> has {role1.card} of type <class1.name>.
# Une|Une <Class2.name> a {role1.card} de type <class1.name>
# A "File" has {zero or one} "parent" of type "Directory"
# Un "Fichier" a {zero ou un} "parent" de type "Directory
#
# Constraints.
# ''''''''''''
#
# If <var2> {role2.card} <role2.name> of a <Class1.name> <var1>
#     then <var1> {role1.card} <role1.name> of [the <Class2.name>] <var1>
# Si <var2> {role2.card} <role2.name> d'un|d'une <Class1.name> <var1>
#     alors <var1> {role1.card} <role1.name> of [de le|la <Class2.name>] <var1>
#
# The opposite constraints are necessary on both direction.
#
# {Cardinalities}
#
#     [0/..1]
#         is the
#         est le|la
#     [0..*]
#         is one of the
#         est l'un|une des
#
# example 1: assoc 11:
#     propriete : Maison[1]  <--> proprietaire : Personne[1]
#
#     If p is the "owner" of a "House" h
#         then m is the "property" of [the "Person"] h.
#     Si p est le "proprietaire" d'une "Maison" m
#         alors m est la "propriete" de [la "Personne" h].
#
# example 2: assoc nn:
#     maisonsVisitees : Maison[*] <--> visiteurs : Personne[*]
#
#     Si m est l'un des "maisonsVisitees" d'une Personne p
#         alors p est l'un des "visiteurs' de [la "Maison"] m.
#

#
#
#
# Examples
# '''''''''''''''''''''''''''
#
# Si f est l'un des "filmJoues" d'une person p alors p est l'un des acteurs de f [????et inversement???]]
#
# Assoc 1-1
#
# ---------------------
#
# Le concept de "Fichier" est important.
# Le concept de "FichierPlein" est important.
# Le concept de "Repertoire" est important.
# Le "nom" d'un "Fichier" est une chaine.
# La "taille" d'un "fichier" est un entier.
# Un "FichierPlein" est un "Fichier".
# Un "Repertoire" est un "Fichier".
# Un "Repertoire" "Contient " un nombre quelconque de "fichiers" de type "Fichier".
# Un "Repertoire" a un nombre quelconque de "fichiers" de type "Fichier".
# Un "Fichier" a un zero ou un "parent" de type "Repertoire"
#
# Le concept de "Personne" est important.
# Une "Personne" a entre 0 et deux "parents" de type "Personne".
# Une "Personne" a un nombre quelconque d'"enfants" de type "Personne".
# Une "Personne" "EstParent" d'un nombre quelconque d'"enfants" de type "Personne".
# Les "enfants" d'une "Personne"
# Les "parents" d'une Personne ont pour enfants cette personne.
#
# Le concept de "Film" est important.
#
# Film   --- EstRealisePar --- Personne
# Une "Personne" a un nombre quelconque de "filmRealises" de type Film.
# - Un "Film" a un "realisateur" de type "Personne".
# - Un "Film" "EstRealisePar" un "realisateur" de type "Personne".
# * Le "realisateur" d un "Film" f fait partie des "filmsRealises" de f.
# * Les "filmsRealises" de une "Personne" x ont pour "realisateur" x.
#
#
# Une personne a un nombre quelconque de filmJoues de type Film.
# - Un Film a un nombre quelconque de acteur de type Personne.
# - Un Film EstJouePar un nombre quelconque de
#
