@ECHO OFF
rem This proxy batch file is needed for the BAD tests in /test/state

rem %*    = all command line arguments
rem %~dp0 = pathname of this batch file

call "%~dp0\model-start_use.bat" %*