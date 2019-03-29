@ECHO OFF
REM Batch command to run a python program.
REM Change PY_HOME to match your installation..
@set PY_HOME=C:\Users\Fazl\AppData\Local\Programs\Python\Python37-32
@set PY_EXE=%PY_HOME%\python.exe
%PY_EXE% %1 %2 %3 %4 %5 %6 %7 %8 %9
