# coding=utf-8

from typing import Any, Text, Optional, Dict, List

class USEEngine:
    USE_OCL_COMMAND : Text
    out: Optional[Text]
    err: Optional[Text]
    outAndErr: Optional[Text]
    commandExitCode : int

    @classmethod
    def useVersion(cls) -> Text : ...

    @classmethod
    def withUseOCL(cls) -> bool: ...

    @classmethod
    def analyzeUSEModel(cls, useFileName: Text) -> int: ...
    # result separated in 'err' and 'out'

    @classmethod
    def executeSoilFile(cls, modelFile: Text, stateFile: Text)  -> int: ...
    # result in outAndErr as well as temp file returned
    # check cls.commandExitCode


    #-----------------------------------------------------------
    @classmethod
    def __execute(cls, useSource, soilFile, errWithOut=False,
                  executionDirectory=None) -> int:...
    @classmethod
    def __soilHelper(cls, Text) -> Text: ...