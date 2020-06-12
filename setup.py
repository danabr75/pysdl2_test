# https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html
# python setup.py build_ext --inplace
# chmod +x run.c
from setuptools import setup
from Cython.Build import cythonize

import os
from pathlib import Path

directories = ['lib', 'models']
dependencies = ["run.pyx", "manager.pyx"]

root_folder = str(Path(__file__).parent.absolute())
print(root_folder)


for directory in directories:
  path = str(Path(root_folder + "/" + directory))
  print("PATH: " + str(path))
  files = os.listdir(path)
  for f in files:
    if f.endswith(".pyx"):
      print(f)
      dependencies.append(f)

setup(
  ext_modules = cythonize(dependencies)
)