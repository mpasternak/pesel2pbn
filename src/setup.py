# -*- encoding: utf-8 -*-

import sys
sys.path.append("src")

from cx_Freeze import setup, Executable

path_platforms = ( "C:\Python34\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll", "platforms\qwindows.dll" )

includes = ["atexit","PyQt5.QtCore","PyQt5.QtGui", "PyQt5.QtWidgets"]

includefiles = [path_platforms]

excludes = [
    '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
    'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
    'Tkconstants', 'Tkinter'
]

path = []

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "includes":      includes, 
    "include_files": includefiles,
    "excludes":      excludes, 
    "path":          path
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
exe = None

if sys.platform == "win32":
    exe = Executable(
        script="C:/code/pesel2pbn/src/pesel2pbn/main.py",
        initScript = None,
        base="Win32GUI",
        targetName="pesel2pbn.exe",
        compress = True,
        copyDependentFiles = True,
        appendScriptToExe = False,
        appendScriptToLibrary = False,
        icon = None
    )

setup(  
    name = "pesel2pbn",
    version = "0.1",
    author = 'Michał Pasternak',
    packages = ["pesel2pbn"],
    description = "PESEL2PBN",
    options = {"build_exe": build_exe_options},
    executables = [exe]
)
