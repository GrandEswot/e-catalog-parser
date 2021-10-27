from cx_Freeze import setup, Executable

setup(
    name = "название проги",
    version = "1.0",
    description = "описание - необязательно",
    executables = [Executable("free.py")]
)