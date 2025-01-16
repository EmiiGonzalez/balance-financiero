# setup.py
from cx_Freeze import setup, Executable

setup(
    name="Gestor_Financiero",
    version="1.0",
    description="Aplicación de gestión financiera personal",
    executables=[Executable("financial-manager.py", base="Win32GUI")],
    options={
        "build_exe": {
            "includes": [
                "tkinter",
                "matplotlib",
                "numpy",  
                "datetime",
                "csv",
                "json",
                "os"
            ],
            "include_files": [
                "config.json",
                "icono.png"
            ]
        }
    }
)