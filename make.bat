@echo off
cd src
python.exe setup.py build
cd ..

"%PROGRAMFILES%\Inno Setup 5\ISCC.exe" pesel2pbn.iss