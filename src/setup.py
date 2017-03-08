# -*- encoding: utf-8 -*-

import sys
import os
from cx_Freeze import setup, Executable

from pesel2pbn.version import VERSION

base = None
targetName = "pesel2pbn.app"
include_files = []

def api_ms_win_missing_includes():
    for elem in ["core-file-l1-2-0.dll",
                 "core-file-l2-1-0.dll",
                 "core-localization-l1-2-0.dll",
                 "core-processthreads-l1-1-1.dll",
                 "core-synch-l1-2-0.dll",
                 "core-timezone-l1-1-0.dll",
                 "core-xstate-l2-1-0.dll",
                 "crt-conio-l1-1-0.dll",
                 "crt-convert-l1-1-0.dll",
                 "crt-environment-l1-1-0.dll",
                 "crt-filesystem-l1-1-0.dll",
                 "crt-heap-l1-1-0.dll",
                 "crt-locale-l1-1-0.dll",
                 "crt-math-l1-1-0.dll",
                 "crt-multibyte-l1-1-0.dll",
                 "crt-private-l1-1-0.dll",
                 "crt-process-l1-1-0.dll",
                 "crt-runtime-l1-1-0.dll",
                 "crt-stdio-l1-1-0.dll",
                 "crt-string-l1-1-0.dll",
                 "crt-time-l1-1-0.dll",
                 "crt-utility-l1-1-0.dll",
                 "eventing-provider-l1-1-0.dll"]:
        yield ((r"%WINDIR%\system32\api-ms-win-" + elem).replace("%WINDIR%", os.getenv("WINDIR")), "api-ms-win-" + elem)

if sys.platform == "win32":
    base="Win32GUI"
    targetName = "pesel2pbn.exe"
    include_files = [
        (r"%USERPROFILE%\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\plugins\platforms\qwindows.dll".replace("%USERPROFILE%", os.getenv("USERPROFILE")), "platforms\qwindows.dll"),

        (r"%WINDIR%\system32\ucrtbase.dll".replace("%WINDIR%", os.getenv("WINDIR")), "ucrtbase.dll"),

        (r"%ProgramFiles%\Internet Explorer\IEShims.dll".replace("%ProgramFiles%", os.getenv("ProgramFiles")), "IEShims.dll"),
        
        (r"%USERPROFILE%\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\bin\concrt140.dll".replace("%USERPROFILE%", os.getenv("USERPROFILE")), "concrt140.dll"),

        ] + list(api_ms_win_missing_includes())


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
