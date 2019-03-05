from setuptools import setup
import sys
import os
import imp
from setuptools import Extension
import platform

dirname = os.path.dirname(__file__)
path_version = os.path.join(dirname, "vaex/core/_version.py")
version = imp.load_source('version', path_version)

name = 'vaex'
author = "Maarten A. Breddels"
author_email = "maartenbreddels@gmail.com"
license = 'MIT'
version = version.__version__
url = 'https://www.github.com/maartenbreddels/vaex'
# TODO: can we do without requests and progressbar2?
# TODO: after python2 supports frops, future and futures can also be dropped
# TODO: would be nice to have astropy only as dep in vaex-astro
install_requires_core = ["numpy>=1.11", "astropy>=2", "aplus", "tabulate",
                         "future>=0.15.2", "pyyaml", "progressbar2", "psutil>=1.2.1",
                         "requests", "six", "cloudpickle", 'pybind11>=2.2']
if sys.version_info[0] == 2:
    install_requires_core.append("futures>=2.2.0")
install_requires_viz = ["matplotlib>=1.3.1", ]
install_requires_astro = ["kapteyn"]


class get_numpy_include(object):
    """Helper class to determine the numpy include path
    The purpose of this class is to postpone importing numpy
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self):
        pass

    def __str__(self):
        import numpy as np
        return np.get_include()

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

if platform.system().lower() == 'windows':
    extra_compile_args = ["/EHsc"]
else:
    extra_compile_args = ["-std=c++14", "-mfpmath=sse", "-O3", "-funroll-loops"]

# on windows (Conda-forge builds), the dirname is an absolute path
extension_vaexfast = Extension("vaex.vaexfast", [os.path.relpath(os.path.join(dirname, "src/vaexfast.cpp"))],
                               include_dirs=[get_numpy_include()],
                               extra_compile_args=extra_compile_args)
extension_strings = Extension("vaex.strings", [os.path.relpath(os.path.join(dirname, "src/strings.cpp"))],
                               include_dirs=[get_numpy_include(), get_pybind_include(), get_pybind_include(user=True)],
                               extra_compile_args=extra_compile_args)

setup(name=name + '-core',
      version=version,
      description='Core of vaex',
      url=url,
      author=author,
      author_email=author_email,
      setup_requires=['numpy'],
      install_requires=install_requires_core,
      license=license,
      package_data={'vaex': ['test/files/*.fits', 'test/files/*.vot', 'test/files/*.hdf5']},
      packages=['vaex', 'vaex.core', 'vaex.file', 'vaex.test', 'vaex.ext', 'vaex.misc'],
      ext_modules=[extension_vaexfast, extension_strings],
      zip_safe=False,
      entry_points={
          'console_scripts': ['vaex = vaex.__main__:main'],
          'gui_scripts': ['vaexgui = vaex.__main__:main']  # sometimes in osx, you need to run with this
      }
      )
