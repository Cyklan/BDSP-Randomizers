import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only

build_exe_options = {
    "packages": [
        "os", 
        "configparser",
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "Randomizers",
        "AdditionalMods",
        "Utilities",
        "AtmospherePaths",
        "UnityPy",
        "PIL",
        "antlr4",
        "keystone",
        "tkinter",
    ],
    "excludes": [ 
        "sqlite3", 
        "scipy.lib.lapack.flapack", 
        "PyQt4",
        "PyQt5.QtQml",
        "PyQt5.QtQuick",
        "PyQt5.QtWebEngine",
        "PyQt5.QtWebEngineWidgets",
        "PyQt5.QtBluetooth",
        "PyQt5.QtDBus",
        "PyQt5.QtDesigner",
        "PyQt5.QtHelp",
        "PyQt5.QtLocation",
        "PyQt5.QtMultimedia",
        "PyQt5.QtMultimediaWidgets",
        "PyQt5.QtNfc",
        "PyQt5.QtOpenGL",
        "PyQt5.QtPositioning",
        "PyQt5.QtPrintSupport",
        "PyQt5.QtSensors",
        "PyQt5.QtSerialPort",
        "PyQt5.QtSql",
        "PyQt5.QtSvg",
        "PyQt5.QtTest",
        "PyQt5.QtWebChannel",
        "PyQt5.QtWebSockets",
        "PyQt5.QtXml",
        "PyQt5.QtXmlPatterns",
        "numpy.core._dotblas", 
        "numpy", 
        "matplotlib", 
        "PyTorch"
    ],
    "include_files": [
        "BDSP.png", 
        "Resources", 
        "saves", 
        "rando.ini.example",
        "mainwindow.ui",
        "RandomizerIcon.png"
    ],
    "includes": [
        "Randomizers",
        "AdditionalMods",
        "Utilities",
        "AtmospherePaths",
        "asm"
    ],
    "optimize": 2
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "BDSP Randomizers",
    version = "1.0",
    description = "A randomizer for Brilliant Diamond/Shining Pearl!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, icon="RandomizerIcon.png")]
)
