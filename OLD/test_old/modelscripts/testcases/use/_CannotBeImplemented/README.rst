Cannot be implemented
=====================

This directory contains use files that cannot be implemented with a regexp line parser

Another example which is ambiguous with a line parser with no indentation:

    class X
    operations
       op(
         )
         pre:
           op()
    end

train.use
---------

Operations with signatures on various lines produce errors::

    PyUseOCL parser: cannot process line #81: "  overlaps( a1: Station, a2: Station,"
    PyUseOCL parser: cannot process line #82: "            b1: Station, b2: Station ) : Boolean ="



t015.use
--------

Operations signature on multiple lines::

      overlaps( a1: Bahnhof, a2: Bahnhof,
                b1: Bahnhof, b2: Bahnhof ) : Boolean =

t051.use
--------

Context that do not fit on line lines produce errors::

    context Travail::getListeTravauxAvecGrille(etu : Personne, note: Integer) :
    Set(Travail)
       pre : note >=0 and note <=100


t078.use
--------

Context on multiple lines::

    context Book::
      init(aTitle:String, anAuthSeq:Sequence(String), aYear:Integer)