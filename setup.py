# setuptools installation of GromacsWrapper
# Copyright (c) 2008-2011 Oliver Beckstein <orbeckst@gmail.com>
# Released under the GNU Public License 3 (or higher, your choice)
#
# See the files INSTALL and README for details or visit
# http://sbcb.bioch.ox.ac.uk/oliver/software/GromacsWrapper/
from __future__ import with_statement

#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

# Dynamically calculate the version based on gromacs.VERSION.
# (but requires that we can actually import the package BEFORE it is
# properly installed!)
version = __import__('grom').get_version()

setup(name="grom",
      version=version,
      description="Gromacs parameter editor with syntax highlighting and pdb,gro table editor",
      long_description=long_description,
      author="Hovakim Grabski",
      author_email="hovakim_grabski@yahoo.com",
      license="GPLv3",
      url="://github.com/hovo1990/GROM",
      download_url="https://github.com/hovo1990/GROM/downloads",
      keywords="science Gromacs Editor Parameter PDB GRO Syntax Highlighting Visual Cues 'molecular dynamics'",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: GUI',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: POSIX',
                   'Operating System :: Windows :: Windows',
                   'Programming Language :: Python3',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Chemistry',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3'
                   ],
      packages=find_packages(include=['exampleFiles','documentation']),
      package_data={'grom': ['tableWidget/*.py', 'textWidget/*.py',  # template files
                                'ui/*.py','./*.py'],                                      # server start in VMD
                    },
      install_requires = [
                          'pyenchant',        # numkit needs it
                          ],              # basic package (w/o analysis),
      zip_safe = True,
)


