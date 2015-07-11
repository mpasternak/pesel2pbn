@echo off
cd src
\python34\python.exe setup.py build
cd ..

"c:\Program Files (x86)\Inno Setup 5\ISCC.exe" pesel2pbn.iss