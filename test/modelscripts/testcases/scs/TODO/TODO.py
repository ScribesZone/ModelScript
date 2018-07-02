# TODO: check that there is only one class metamodel imported
#   since a story interpret the object model with respect to the
#   current class model, it could be different from the class model
#   used to validate the object model. It can therefore give less
#   or more errors such as cardinality or so.
#   Currently the error seems to be ok, but it is most certainly
#   better to send a, error message if there is more than one
#   class model imported.