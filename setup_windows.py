from cx_Freeze import setup, Executable

exe = Executable(
    script="GROM.py",
    base="Win32GUI",
    icon="icon.ico"
    )


includefiles=["documentation/","exampleFiles/"]

setup(
    name = "GROM",
    version = "0.5",
    author = "Hovakim Grabski",
    description = "GROM editor",
    options = {'build_exe': {'include_files':includefiles}},
    executables = [exe]
    )
