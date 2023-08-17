from setuptools import setup, find_packages


# Metadatos del proyecto
name = "alanube"
version = "0.0.0"
author = "Wilmer Martinez"
description = "Library to establish connections with the Alanube API."
url = "https://github.com/wilmerm/alanube-python"
license = "MIT"

# Archivos que se incluirán en la distribución
packages = find_packages()

# Dependencias (si las hay)
install_requires = [
    'requests',
]

# Configuración del setup
setup(
    name=name,
    version=version,
    author=author,
    description=description,
    url=url,
    license=license,
    packages=packages,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
