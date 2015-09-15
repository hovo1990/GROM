GROM

version: 0.6.9

GROM is a GROMACS(mdp,itp,top) files with Syntax Highlighting and PDB Editor wtih visual cues in one package based on Qt5,PyQt5 and Python3. It's GPL licensed!(See LICENSE)

Dependencies

Python >= 3.0 (or Python3)

PyQt >= 5.0

License

GPLv3+ (GPLv3 or any other version later published by FSF at your option)

**New Features**


Now you can connect your RS232 device, e.g. Spectrometer(Tested with Jenway 6405)
![Alt text](/screenshots/screen14.png?raw=true "Screen 14")




Screenshots:

![Alt text](/screenshots/screen1.png?raw=true "Screen 1")
![Alt text](/screenshots/screen2.png?raw=true "Screen 2")
![Alt text](/screenshots/screen7.png?raw=true "Screen 7")
![Alt text](/screenshots/screen8.png?raw=true "Screen 8")
![Alt text](/screenshots/screen9.png?raw=true "Screen 9")
![Alt text](/screenshots/screen3.png?raw=true "Screen 3")
![Alt text](/screenshots/screen4.png?raw=true "Screen 4")
![Alt text](/screenshots/screen5.png?raw=true "Screen 5")
![Alt text](/screenshots/screen6.png?raw=true "Screen 6")
![Alt text](/screenshots/screen10.png?raw=true "Screen 10")
![Alt text](/screenshots/screen11.png?raw=true "Screen 11")
![Alt text](/screenshots/screen12.png?raw=true "Screen 12")
![Alt text](/screenshots/screen13.png?raw=true "Screen 13")

Before you run it:


    Please Install Qt5, Pyqt5 and Python3:
        On Ubuntu:
            sudo apt-get install build-essential
            sudo apt-get install python3
            sudo apt-get install qt5-default qttools5-dev-tools
            sudo apt-get install python3-pyqt5
            sudo apt-get install libqt5webkit5
            sudo apt-get install python3-pyqt5.qtwebkit
            sudo apt-get install python3-pip #Install pip
            sudo pip3 install pyenchant # For spelling Suggestion of Parameters
            sudo pip3 install pyserial # For RS232 connection


        On Windows:
        if 64 bit, find, download and install:
            python-3.4.3.amd64.msi
            PyQt5-5.4.2-gpl-Py3.4-Qt5.4.2-x64.exe
            numpy-1.9.2+mkl-cp34-none-win_amd64.whl
            scipy-0.16.0-cp34-none-win_amd64.whl
            matplotlib-1.4.3.win-amd64-py3.4.
            pip3 install pyenchant # For spelling Suggestion of Parameters
            pip3 install pyserial # For RS232 connection


And run it:

.. code:: bash
    $ python3 GROM.py




Author:2014 by Hovakim Grabski(hovakim_grabski@yahoo.com,johnwo1990@hotmail.com)
