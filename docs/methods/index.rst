.. _ModelScriptMethod:

Methods
=======

ModelScript comes with a simple method, the "ModelScript Method".
Strictly speaking instead of one method, this is a set of methods since
some method elements can be added or removed.

The method is decomposed in (1) tasks and (2) artefacts to be used/produced
by eash tasks. The method is modular in the sense that only a
few artefacts and/or steps can be used.

The method is based on a project layout for modeling *artefacts*.
It also relies on a set of tasks to be performed for the *process*.
Each tasks have to be concluded by an status file, a file which is not
currently written as a script.

:download:`ModelScript CheatSheet <../dist/ModelScript-CheatSheet.pdf>`

..  toctree::
    :maxdepth: 3

    artefacts

    concepts/index
    bd/index
    cu/index
    ihm/index
    projet/index
    dev/index

..  _`ModelScript CheatSheet`:


..  |umlOclCheatSheet| replace::
    (:download:`local<docs/UMLOCL-CheatSheet-18.pdf>`)