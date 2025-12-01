from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import platform

# Configuración específica por plataforma
if platform.system() == "Windows":
    extra_compile_args = ["/O2", "/EHsc"]
    extra_link_args = []
    define_macros = [("_CRT_SECURE_NO_WARNINGS", None)]
else:
    extra_compile_args = ["-std=c++11", "-O3"]
    extra_link_args = []
    define_macros = []

# Extensión de Cython
extensions = [
    Extension(
        "wrapper",
        sources=["src/wrapper.pyx", "src/grafo.cpp"],
        include_dirs=["src"],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=define_macros,
    )
]

setup(
    name="NeuroNet",
    version="1.0",
    description="Sistema de Análisis de Grafos Masivos",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)

print("\n" + "="*60)
print("INSTRUCCIONES DE COMPILACIÓN:")
print("="*60)
print("1. Ejecuta: python setup.py build_ext --inplace")
print("2. Luego ejecuta la GUI: python gui.py")
print("="*60 + "\n")