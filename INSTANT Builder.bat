@echo off
color 0F
cls

echo.                                                                                                                                                                                                       
echo    db    88 88""Yb 88        db    88   88 88b 88  dP""b8 88  88     88""Yb 88   88 88 88     8888b.  888888 88""Yb 
echo   dPYb   88 88__dP 88       dPYb   88   88 88Yb88 dP   `" 88  88     88__dP 88   88 88 88      8I  Yb 88__   88__dP 
echo  dP__Yb  88 88"Yb  88  .o  dP__Yb  Y8   8P 88 Y88 Yb      888888     88""Yb Y8   8P 88 88  .o  8I  dY 88""   88"Yb  
echo dP""""Yb 88 88  Yb 88ood8 dP""""Yb `YbodP' 88  Y8  YboodP 88  88     88oodP `YbodP' 88 88ood8 8888Y"  888888 88  Yb                  
echo Version 0.19, Build 33 
echo.                                                                                                
echo This builder should come pre-packed with the zip/source code that contains
echo the MAIN.PY file with the program.
echo.
echo If you don't know what this version does, please check The normal builder.bat.
echo.
echo Please CONFIRM that you have the following Python dependencies:
echo - Python 3.14.x (preferably 3.14.2)
echo - Pillow 12.1.0+
echo - PyWin32 311+
echo - Tkinter 8.6.x (should come pre-installed with Python)
echo - PyInstaller 6.18.x (Preferrably 6.18.0)
echo.
echo.
echo Press any key to begin building...
pause >nul
echo.
echo Compiling...
timeout /t 1 /nobreak >nul

:: Run PyInstaller on MAIN.PY in the current directory
"%LOCALAPPDATA%\Programs\Python\Python314\Scripts\pyinstaller.exe" "%~dp0MAIN.PY" --windowed --onefile -n airLaunch -i "%~dp0appicon.ico"

echo.
echo Press any key to exit.
pause >nul
exit
