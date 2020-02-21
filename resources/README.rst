Methods
=======

This directory contains a template implementing a modeling method.
Currently there is only one "all-in-one" method. Customization could
be done by selecting/adapting individual components.

classroom-hq
------------

This directory contains skeletons for assignments. Search and replace
all instances of XXX. In particular XXX-CASESTUDY has to be renamed
to the name of the casestudy. XXX-COLOR has to be replaced by
a color (e.g. "2f00ff") associated to git issue.

Since the content of the assignments are not specific to the casestudy
(just the title), the assignments can ba directly copied to the
instance of the casestudy, in a given classroom. This avoid to
have unecessaru copies and back-port problems.

classrooms-root
---------------

This directory contains skeletons of the file structure to be
distributed to students. Search and replace all instances of XXX
in particular directories named XXX-CASESTUDY. When creating/updating
a case study, the content of the ``casestudy-specific`` has to be merged
manually.
