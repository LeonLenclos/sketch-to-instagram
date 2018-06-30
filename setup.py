import sys
from cx_Freeze import setup, Executable

setup(
    name = "Sketch To Instagram",
    version = "1.0",
    description = "Draw simple sketch and share it on Instagram",
    executables = [Executable("sti.py")])
