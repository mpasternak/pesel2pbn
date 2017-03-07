# -*- encoding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

from pesel2pbn.version import VERSION

base = None
targetName = "pesel2pbn.app"

if sys.platform == "win32":
    base="Win32GUI"
    targetName = "pesel2pbn.exe"


exe = Executable(
    script="pesel2pbn/main.py",
    initScript = None,
    base=base,
    targetName=targetName,
    compress=True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = None
    )

setup(
    name = "pesel2pbn",
    version = VERSION,
    author = 'Michal Pasternak',
    packages = ["pesel2pbn"],
    description = "PESEL2PBN",
    options = {
        "build_exe": {
            "include_msvcr": True,   #skip error msvcr100.dll missing
            "packages": ['pesel2pbn',],
            "includes": [
                "atexit",
                "PyQt5.QtCore",
                "PyQt5.QtGui",
                "PyQt5.QtWidgets",
                "pesel2pbn.pesel2pbn_auto"
            ],
            "include_files": [
                ("C:\Python34\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll",
                 "platforms\qwindows.dll" )
                ],
            "excludes": [
                '_gtkagg',
                '_tkagg',
                'bsddb',
                'curses',
                'email',
                'pywin.debugger',
                'pywin.debugger.dbgcon',
                'pywin.dialogs',
                'tcl',
                'Tkconstants',
                'Tkinter'],            
        }               
    },
    executables = [exe]
)
