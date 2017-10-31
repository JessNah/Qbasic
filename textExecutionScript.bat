@echo off

Setlocal EnableDelayedExpansion

call :parseFile
goto :eof

REM :directoryTraversal
rem Entering login
REM cd Testing
REM cd LOGIN
REM cd Input Files


REM for %%f in (*.txt) do (
    rem echo %%f
REM	SET fi=%%f
REM	set fi=!fi:input=output!
REM	echo !fi!
REM	)

:ParseFile
for /F "tokens=*" %%A in (testsToRun.txt) do (
	set "List=%%A"
	goto :NextItem
	echo %input%
	echo %transaction%
	echo %output%
)
goto eof

:NextItem
if "%List%" == "" goto :print

set /A ItemCount+=1
for /F "tokens=1* delims=," %%a in ("%List%") do (
    echo Item %ItemCount% is: %%a
    set "List=%%b"
	
	if %ItemCount%==2 set input=%%a
	if %ItemCount%==3 set transaction=%%a
	if %ItemCount%==4 set output=%%a
	
)
goto NextItem

:print
echo %input%
echo %transaction%
echo %output%
pause
goto parseFile

pause
exit /b