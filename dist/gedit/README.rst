GEdit - Syntax Highligting
==========================

This directory contains resources to add Syntax Highlighting for
ModelScript languages.

Language specification
----------------------

The content of the ``language-specs`` directory should be copied to
the directory ``~/.local/share/gtksourceview-3.0/``.
You may have to create parent directories if they do not exist.

**Alternatively**, if you don't want to to copy this directory you can
create a symbolic link from your home directory to the installation
directory::

    cd ~/.local/share/gtksourceview-3.0/
    ln -s PATH_TO_INSTALL_DIR/dist/gedit/language-specs/ .

Style specification
-------------------

The content of the ``style`` directory should be copied to the
directory ``~/.local/share/gedit/``. You may have to create parent
directories if they do not exist.

**Alternatively**, if you don't want to to copy this directory you can
create a symbolic link from your home directory to the installation
directory::

    cd ~/.local/share/gedit
    ln -s PATH_TO_INSTALL_DIR/dist/gedit/language-specs/ .

Tools
-----

GEdit tools are commands that can be run from the editore. Tools
are defined in the following directory::
