@echo off
color 0F
cls

echo.                                                                                                                                                                                                       
echo    db    88 88""Yb 88        db    88   88 88b 88  dP""b8 88  88     88""Yb 88   88 88 88     8888b.  888888 88""Yb 
echo   dPYb   88 88__dP 88       dPYb   88   88 88Yb88 dP   `" 88  88     88__dP 88   88 88 88      8I  Yb 88__   88__dP 
echo  dP__Yb  88 88"Yb  88  .o  dP__Yb  Y8   8P 88 Y88 Yb      888888     88""Yb Y8   8P 88 88  .o  8I  dY 88""   88"Yb  
echo dP""""Yb 88 88  Yb 88ood8 dP""""Yb `YbodP' 88  Y8  YboodP 88  88     88oodP `YbodP' 88 88ood8 8888Y"  888888 88  Yb                  
echo Version 0.19, Build 26                                                                                                  
echo This builder should come pre-packed with the zip/source code that contains
echo the MAIN.PY file with the program.
echo.
echo This tool can be used for building other apps, but doing so is not recommended.
echo Support for non-airLaunch apps is at your own risk.
echo.
pause
echo.
echo If you are a normal user seeking to directly start using this app now, please use the exe
echo on the GitHub download for convenience.
echo.
echo Please CONFIRM that you have the following Python dependencies:
echo - Python 3.14.x (preferably 3.14.2)
echo - Pillow 12.1.0+
echo - PyWin32 311+
echo - Tkinter 8.6.x (should come pre-installed with Python)
echo - PyInstaller 6.18.x (Preferrably 6.18.0)
echo.
pause
echo.
set /p answer=Do you have all dependencies installed? [Y/N]: 

if /i "%answer%"=="Y" goto BUILD
if /i "%answer%"=="N" goto EXIT

:BUILD
cls
echo    db    88 88""Yb 88        db    88   88 88b 88  dP""b8 88  88     88""Yb 88   88 88 88     8888b.  888888 88""Yb 
echo   dPYb   88 88__dP 88       dPYb   88   88 88Yb88 dP   `" 88  88     88__dP 88   88 88 88      8I  Yb 88__   88__dP 
echo  dP__Yb  88 88"Yb  88  .o  dP__Yb  Y8   8P 88 Y88 Yb      888888     88""Yb Y8   8P 88 88  .o  8I  dY 88""   88"Yb  
echo dP""""Yb 88 88  Yb 88ood8 dP""""Yb `YbodP' 88  Y8  YboodP 88  88     88oodP `YbodP' 88 88ood8 8888Y"  888888 88  Yb
echo.
echo Great! Make sure MAIN.PY is in the same folder as this batch file.
echo.
pause
echo Please confirm you want to build airLaunch.
pause
echo Press any key to begin building...
pause >nul

:: 5-second countdown loop
for /l %%i in (5,-1,1) do (
    cls
    echo Building in %%i...
    timeout /t 1 /nobreak >nul
)

echo.
echo Compiling...
timeout /t 1 /nobreak >nul

:: Run PyInstaller on MAIN.PY in the current directory
"%LOCALAPPDATA%\Programs\Python\Python314\Scripts\pyinstaller.exe" "%~dp0MAIN.PY" --windowed --onefile -n airLaunch -i "%~dp0appicon.ico"

echo.
echo Building finished. You can save the log if needed.
pause
echo Press any key to exit.
pause >nul
exit

:EXIT
echo.
echo Press any key to exit the batch file...
pause >nul
exit
