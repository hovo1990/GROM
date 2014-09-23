

# -*- coding: utf-8 -*-
#
# This file is part of GROM.
#
# GROM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# GROM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GROM; If not, see <http://www.gnu.org/licenses/>.



###############################################################################
# DOC
###############################################################################
 #!/usr/bin/env python3


"""
GROM
-----

GROM is a GROMACS(mdp,itp,top)  with Syntax Highlighting and PDB Editor with visual cues in one package  based on Qt5,PyQt5 and Python3.
It's GPL licensed!(See LICENSE)


Before you run it:
`````````````````

    Please Install Qt5, Pyqt5 and Python3:
        On Ubuntu:
            sudo apt-get install build-essential
            sudo apt-get install python3
            sudo apt-get install qt5-default qttools5-dev-tools
            sudo apt-get install python3-pyqt5
            sudo apt-get install libqt5webkit5
            sudo apt-get install python3-pyqt5.qtwebkit


And run it:

.. code:: bash
    $ python3 GROM.py

"""
###############################################################################
# IMPORTS
###############################################################################

import grom


###############################################################################
# MAIN
###############################################################################


if __name__ == "__main__":
    grom.setup_and_run()
