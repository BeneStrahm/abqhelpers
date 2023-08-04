for %%I in (.) do set CurrDirName=%%~nxI
echo %CurrDirName%

set "target=H:\Strahm\Abaqus"

robocopy . %target%\%CurrDirName% /DCOPY:DAT /R:10 /W:3 *.inp
robocopy . %target%\%CurrDirName% /DCOPY:DAT /R:10 /W:3 *.py

pause