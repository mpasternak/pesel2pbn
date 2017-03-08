@echo off
cd src

rmdir /s /q build

cd pesel2pbn
pyuic5 pesel2pbn.ui > pesel2pbn_auto.py
cd ..

python.exe setup.py build
cd ..

"%PROGRAMFILES%\Inno Setup 5\ISCC.exe" pesel2pbn.iss