for %%I in (.) do set CurrDirName=%%~nxI
echo %CurrDirName%

set path=H:\Strahm\Abaqus

robocopy . %path%\%CurrDirName% /DCOPY:DAT /R:10 /W:3 *.inp
robocopy . %path%\%CurrDirName% /DCOPY:DAT /R:10 /W:3 *.py

pause