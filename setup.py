from cx_Freeze import setup, Executable

include_files = ['data']

options = {
    'build_exe': {
        'include_msvcr': True,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(
    name="название проги",
    version="1.0",
    description="описание - необязательно",
    executables=[Executable("main.py")],
    options=options,
)
