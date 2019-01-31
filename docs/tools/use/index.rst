USE
===

The current version of ModelScript depends on the USE_ tool from the
university of bremen. USE_ allows to check consistency between object
and class models, as well as drawing UML diagrams.

Checking classes consistency::

    use -c classes/classes.cl1

Checking classes/objects consistency::

    use -qv classes/classes.cl1 objects/o1/o1.ob1

Creating a class diagram using the graphical interface::

    use classes/classes.cl1 objects/o1/o1.ob1

Creating an object diagram using the graphical interface::

    use classes/classes.cl1 objects/o1/o1.ob1

Using the command line interpreter::

    use -nogui classes/classes.cl1 objects/o1/o1.ob1


..  _`USE`: https://scribetools.readthedocs.io/en/latest/useocl/index.html




