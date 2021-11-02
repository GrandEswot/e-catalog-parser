from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='parser.exe',
                          )
               ]

include_files = ['data']

options = {
    'build_exe': {
        'include_msvcr': True,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='parser',
      version='0.0.13',
      description='e-catalog.ru parser',
      executables=executables,
      options=options)
