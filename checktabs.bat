@ECHO OFF
REM Batch command to check a python program for ambiguous indentation
REM Change PY_HOME to match your installation..
@set PY_HOME=C:\Users\Fazl\AppData\Local\Programs\Python\Python37-32
@set PY_EXE=%PY_HOME%\python.exe
%PY% %PY_HOME%\lib\tabnanny.py -v %1
