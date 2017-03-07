# -*- encoding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

from pesel2pbn.version import VERSION

base = None
targetName = "pesel2pbn.app"
include_files = None

if sys.platform == "win32":
    base="Win32GUI"
    targetName = "pesel2pbn.exe"
    include_files = [
        ("%USERPROFILE%\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\plugins\platforms\qwindows.dll",
         "platforms\qwindows.dll" )
        ],


exe = Executable(
    script="pesel2pbn/main.py",
    initScript = None,
    base=base,
    targetName=targetName,
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
            "include_files": include_files,
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
