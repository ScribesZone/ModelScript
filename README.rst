ModelScript
===========

ModelScript is a textual modeling environment based on a dozen of textual
modeling languages some being textual forms of UML, some other
being textual DSLs.


Installation
------------

1. Download this repository.

2. Enter the ModelScript directory

    cd ModelScript

2. Create a virtual environment and install dependencies.

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

3. Set bin/ files as executable

    chmod +x bin/*

4. Add ...ModelScript/bin/ in your PATH  (change .bashrc)

5. To check if modelc works:

    modelc --version
