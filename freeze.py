import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

exe = Executable(
    script="GROM.py",
    base=base,
    icon="icon.ico"
)

includefiles = ["documentation/", "exampleFiles/"]

setup(
    name="GROM",
    version="0.5",
    author="Hovakim Grabski",
    description="GROM is a Gromacs parameter(.mdp,.itp,.top) Text and .pdb  Table Editor ",
    options={'build_exe': {'include_files': includefiles}},
    executables=[exe]
)
