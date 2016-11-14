## -*- coding: utf-8 -*-


import numpy as np
import xdrlib
import difflib
import os
import difflib


class FeatureNotAvailable(Exception):
    pass


class IOHandler(object):
    """Generic base class for file readers and writers.

    The initialization function takes a file-like object *fd*, as an
    argument.

    Subclasses can extend the methods *__init__*, *read* and *write*
    to implement their reading and writing routines.

    **Attributes**

    .. py:attribute:: fd

    .. py:attribute:: IOHandler.can_read

        :type: list of str

        A list of *features* that the handler can read.

    .. py:attribute:: IOHandler.can_write

        :type: list of str

        A list of *features* that IOHandler can write.

    """

    can_read = []
    can_write = []

    def __init__(self, fd):
        # TODO: This is a deprecation warning
        if isinstance(fd, str):
            raise Exception("IOHandler takes a file-like object as its first argument")

        self.fd = fd

    def read(self, feature, *args, **kwargs):
        """Read and return the feature *feature*. It should raise an
        ValueError if the feature is not present in the handler
        *can_read* attribute, use the method
        :py:meth:`IOHandler.check_feature` to provide this behaviour.

        Certain features may require additional arguments, and it is
        possible to pass those as well.

        **Example**

        Subclasses can reimplement this method to add functionality::

            class XyzIO(IOHandler):
                can_read = ['molecule']

                def read(self, feature, *args, **kwargs):
                    self.check_feature(feature, "read")
                    if feature == 'molecule':
                       # Do stuff
                       return geom

        """

        self.check_feature(feature, "read")

    def write(self, feature, value, *args, **kwargs):
        """Same as  :py:meth:`~chemlab.io.iohandler.IOHandler.read`. You have to pass
        also a *value* to write and you may pass any additional
        arguments.

        **Example**

        ::

            class XyzIO(IOHandler):
                can_write = ['molecule']

                def write(self, feature, value, *args, **kwargs):
                    self.check_feature(feature, "write")
                    if feature == 'molecule':
                       # Do stuff
                       return geom

        """
        if 'w' not in self.fd.mode and 'x' not in self.fd.mode:
            raise Exception(
                "The file is not opened in writing mode. If you're using datafile, add the 'w' option.\ndatafile(filename, 'w')")

        self.check_feature(feature, "write")

    def check_feature(self, feature, readwrite):
        """Check if the *feature* is supported in the handler and
        raise an exception otherwise.

        **Parameters**

        feature: str
            Identifier for a certain feature.
        readwrite: "read" or "write"
            Check if the feature is available for reading or writing.

        """

        if readwrite == "read":
            features = self.can_read
        if readwrite == "write":
            features = self.can_write

        if feature not in features:
            matches = difflib.get_close_matches(feature, features)
            raise FeatureNotAvailable("Feature %s not present in %s. Close matches: %s"
                                      % (feature, str(type(self).__name__),
                                         str(matches)))


class FormatNotSupported(ValueError):
    pass


def make_ionotavailable(name, msg, can_read=[], can_write=[]):
    def read(self, feature):
        raise Exception(msg)

    def write(self, feature):
        raise Exception(msg)

    new_class = type(name, (IOHandler,), {
        'can_read': can_read,
        'can_write': can_write,
        'read': read,
        'write': write
    })

    return new_class


def remotefile(url, format=None):
    """The usage of *remotefile* is equivalent to
    :func:`chemlab.io.datafile` except you can download a file from a
    remote url.

    **Example**

        mol = remotefile("https://github.com/chemlab/chemlab-testdata/blob/master/3ZJE.pdb").read("molecule")

    """

    if format is None:
        res = urlparse(url)
        filename, ext = os.path.splitext(res.path)

        hc = get_handler_class(ext)
    else:
        hc = _handler_map.get(format)
        if hc is None:
            raise ValueError('Format {} not supported.'.format(format))

    fd = urlopen(url)
    handler = hc(fd)
    return handler


class QuantityNotAvailable(Exception):
    pass


class EdrIO(IOHandler):
    '''EDR files store per-frame information for gromacs
    trajectories. Examples of properties obtainable from EDR files are::

    - temperature
    - pressure
    - density
    - potential energy
    - total energy
    - etc.

    To know which quantities are available in a certain edr file you
    can access the feature 'avail quantity'::

        >>> datafile('ener.edr').read('avail quantities')
        ['Temperature', 'Pressure', 'Potential', ...]

    To get the frame information for a certain quantity you may use
    the "quantity" property passing the quantity as additional
    argument, this will return two arrays, the first is an array of
    times in ps and the second are the corrisponding quantities::

        >>> time, temp = datafile('ener.edr').read('quantity', 'Temperature')

    **Features**

    .. method:: read("quantity", quant)

        Return an array of times in ps and the corresponding quantities
        at that times.

    .. method:: read("avail quantities")

        Return the available quantities in the file.

    .. method:: read("units")

        Return a dictionary where the keys are the quantities and
        the value are the units in which that quantity is expressed.

    .. method:: read("frames")

        Return a dictionary where the keys are the quantities and
        the value are the units in which that quantity is expressed.


    '''

    can_read = ['quantity', 'units', 'avail quantities']
    can_write = []

    def __init__(self, filename, decode_mode='float'):
        self.processed = False
        self.fd = open(filename, 'rb')
        super(EdrIO, self).__init__(self.fd)

        self.decode_mode = decode_mode


        # def getProps(self):
        # return self.props

    def read(self, feature, *args):
        self.check_feature(feature, 'read')

        if not self.processed:
            self.frames = frames = self.process_frames()
            self.processed = True
        else:
            frames = self.frames

        # print('props right ',self.props)

        if feature == 'units':
            quant = args[0]
            i = self.props.index(quant)
            return self.units[i]

        if feature == 'avail quantities':
            print('tadadadadadad----' * 10)
            return self.props

        if feature == 'quantity':
            if not args[0]:
                raise Exception('the method read("quantity", arg) requires a quantity to get')


                #: not active for now
            quant = args[0]

            if quant not in self.props:
                close = difflib.get_close_matches(quant, self.props)
                raise QuantityNotAvailable('Quantity %s not available. Close matches: %s' %
                                           (str(quant), str(close)))

            time, data = self.dataExtract(quant)

            print('--' * 20)
            print('If data does not make sense, try to run in double decode type')
            print('--' * 20)
            return time, data

            # i = self.props.index(quant)
            # ret = []
            # print('frames is ',frames)
            # for f in frames:
            # print('f is ',f)
            # ret.append(f[i][0])

            # return np.array(self.times), np.array(ret)

    def getUnits(self, row):
        return self.units[row]

    def dataExtractFromRow(self, row):
        i = row
        ret = []
        # print('frames is ',frames)
        for f in self.frames:
            # print('f is ',f) #There's a problem with frames check it out
            ret.append(f[i][0])

        return np.array(self.times), np.array(ret)

    def dataExtract(self, quant):
        i = self.props.index(quant)
        # print('quant is ',quant)
        # print('i is ',i)
        # print(self.props[i])
        #:---------------------------
        ret = []
        # print('frames is ',frames)
        for f in self.frames:
            # print('f is ',f) #There's a problem with frames check it out
            ret.append(f[i][0])

        return np.array(self.times), np.array(ret)

    def process_frames(self):  # This is VERY IMPORTANT

        f = self.fd.read()
        self.up = xdrlib.Unpacker(f)

        if self.decode_mode == "float":  # This is prototype
            self.decJob = self.up.unpack_float
        else:
            self.decJob = self.up.unpack_double

        self.times = [0]
        self.dts = []
        self.frames = []

        self._unpack_MyVersion()
        # self._unpack_start()
        # fr = self._unpack_frame()
        ##print('fr is ',fr)
        ##self.frames.append(fr)


        # while True:
        # fr = self._unpack_frame()
        ##try:
        # fr = self._unpack_frame()
        # except EOFError:
        # print('crap')
        # pass
        # self.frames.append(fr)

        return self.frames

    def _unpack_MyVersion(self):
        print('THis is unpack MyVersion')
        print('---' * 20)
        up = self.up
        magic = up.unpack_int()

        # print('magic at start ',magic)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        self.version = up.unpack_int()
        # print('version ',self.version)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        # Number of properties
        self.nre = up.unpack_int()
        # print('nre is ',self.nre)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        self.props = props = []
        self.units = units = []

        # Strings and units of quantities
        for i in range(self.nre):
            # index = up.unpack_int()
            prop = up.unpack_string()
            unit = up.unpack_string()

            # print('index is ',index)
            # print('prop is ',prop)
            # print('unit is ',unit)
            props.append(prop.decode('utf-8'))
            units.append(unit.decode('utf-8'))

        # print('props ',props)
        # print('units ',units)


        dum = up.unpack_float()  # ???? i guess its a float -20000000000.0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        magic_later = up.unpack_int()
        # print('magic later ',magic_later) #Here is ok -7777777
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # Version--- 5
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')



        dum = up.unpack_int()  # What is this 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this 1
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this 1
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_double()  # What is this 0.002
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks like property number
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 1184
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_float()  # What is this looks 0 -----
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 1184
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')



        #
        # for i in range(self.nre):
        # array = []
        # for y in range(3):
        # value = up.unpack_float() #Value
        ##print('value  --> ',value )
        ##pos = up.get_position()
        ##print('pos is ',pos)
        ##print('------------------')
        # array.append(value)
        ##print('array is ',array)
        # energy.append(array)
        # array = []

        data = []
        array = []
        for i in range(self.nre):  # this is right
            temp = [0, 0, 0]
            # dum = up.unpack_float() #What is this looks it looks its a float
            dum = self.decJob()  # This part decodes
            # print('dum ',dum)
            temp[0] = dum
            # pos = up.get_position()
            # print('pos is ',pos)
            # print('------------------')
            # print('temp is ',temp)
            array.append(temp)
        if len(array) == 0:
            print('fuckus')
        data.append(array)

        try:
            while True:
                temp = self._unpack_timeStep(up)
                if len(temp) == 0:
                    # print('Funcking asshole')
                    print('temp asshole ', temp)
                    print('---------------------')
                data.append(temp)
        except Exception as e:
            print('e is ', e)
            pass

        self.frames = data

        # print('data 0 ',data[0][0])

        # print('data is ',data)
        # print('self.times = ',self.times)
        # print('len ',len(self.times))

    def _unpack_timeStep(self, up):  # The quest right it's for single precision, but what if it's
        # Double Presicision ??????????????????????????
        # print('----------------------One step\n')

        #:--- Header Part
        dum = up.unpack_float()  # What is this looks it looks its a float
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        magic = up.unpack_int()  # What is this  777777777
        # print('magic -->  ',magic)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')



        version = up.unpack_int()  # What is this looks  5
        # print('version --> ',version)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        time = up.unpack_double()  # What is this looks 2.0 maybe time what's wrong
        self.times.append(time)
        # print('time really --> ',time)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        # dum = up.unpack_int() #What is this looks 0.0 Testing
        # print('dum after time',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this looks 0.0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        step = up.unpack_int()  # What is this looks 1000 maybe step
        # print('step --> ',step)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 10 maybe sum steps
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        sumSteps = up.unpack_float()  # What is this looks 10 maybe sum steps
        # print('sumSteps ---> ',sumSteps)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        nsteps = up.unpack_int()  # What is this looks 1000 maybe nsteps
        # print('nsteps --> ',nsteps)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        delta_t = up.unpack_double()  # What is this looks 0.002 maybe delta_t
        # print('delta_t --> ',delta_t)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        self.nre = up.unpack_int()  # What is this looks 74 number of properties
        # print('self.nre --> ',self.nre)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        unknown = up.unpack_int()  # What is this looks 1184 what is this
        # print('uknown   -->',unknown)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')

        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        dum = up.unpack_int()  # What is this looks 0
        # print('dum ',dum)
        # pos = up.get_position()
        # print('pos is ',pos)
        # print('------------------')


        #:-----> Value Part

        try:
            energy = []
            for i in range(self.nre):
                array = []
                for y in range(3):
                    value = self.decJob()  # Value #There are problems
                    # print('value  --> ',value )
                    # pos = up.get_position()
                    # print('pos is ',pos)
                    # print('------------------')
                    array.append(value)
                # print('array is ',array)
                energy.append(array)
                if len(array) == 0:
                    print('Shit man really')
                array = []

            # print(len(energy))
            # eff_array = np.array(energy)
            # print(eff_array)
            return energy
        except Exception as e:
            print('Yikes ', e)
            return 1

    def _unpack_start(self):
        print('THis is unpack start')
        up = self.up
        magic = up.unpack_int()
        print('magic at start ', magic)
        if (magic != -55555):
            raise Exception('Format not supported: magic number -55555 not matching')

        self.version = up.unpack_int()
        print('version ', self.version)

        # Number of properties
        self.nre = up.unpack_int()
        print('nre is ', self.nre)

        self.props = props = []
        self.units = units = []

        # Strings and units of quantities
        for i in range(self.nre):
            # index = up.unpack_int()
            prop = up.unpack_string()
            unit = up.unpack_string()

            # print('index is ',index)
            # print('prop is ',prop)
            # print('unit is ',unit)
            props.append(prop.decode('utf-8'))
            units.append(unit.decode('utf-8'))

            # self._unpack_eheader()

    def _unpack_eheader(self):  # Header part source enxio.c, It does once
        up = self.up

        # data = up.get_buffer()
        # print("packed:", repr(data))

        first_real_to_check = -2e10

        # Checking the first real for format
        first_real = up.unpack_double()
        print('first_real ', first_real)

        # if (first_real != first_real_to_check): #This part also
        # print('tada ',first_real)
        # print('tada fuck ',first_real_to_check )
        # raise Exception('Format not supported, first real not matching.')


        magic = up.unpack_int()
        print('magic is ', magic)
        # if  (magic != -7777777): #This part is important
        # print('magic is ',magic)
        # raise Exception('Format not supported, magic number not matching -7777777')

        version = up.unpack_int()
        time = up.unpack_double()
        self.times.append(time)

        # This two should give us large int that represent the step number
        min = up.unpack_int()

        maj = up.unpack_int()
        print('min is ', min)
        print('max is ', maj)

        self.nsum = up.unpack_int()
        print('nsum is ', self.nsum)

        ## NSTEPS (again?)
        # min = up.unpack_int()
        # print('min is ')
        # maj = up.unpack_int()

        # For version 5
        dt = up.unpack_double()
        print('dt ', dt)
        self.dts.append(dt)

        # Number of properties? Indeed no need for such thing
        self.nre = up.unpack_int()
        print('nre is ', self.nre)

        dum = up.unpack_int()
        print('dum is ', dum)

        nblock = up.unpack_int() + 1
        print('nblock is', nblock)

        # Block headers:
        id = up.unpack_int()
        print('id is ', id)
        nsubblocks = up.unpack_int()
        print('nsubblocks is ', nsubblocks)

        e_size = up.unpack_int()

        print('e_size is ', e_size)
        print('-----' * 20)

        # for i in range(5000):
        # tada = up.unpack_double()
        # print('tada is ',tada)

        # dum = up.unpack_int()
        # dum = up.unpack_int()
        # up.unpack_int()

    def _unpack_frame(self):
        # Energies, averages and rmsd
        self._unpack_eheader()  # for everyframe, 75 and 1184 repeat for every frame

        frame = []

        # for i in range(self.nre):
        # try:
        # en = self.up.unpack_double()
        # print('en is --> ',en)
        ##if self.nsum > 0:
        ##avg = self.up.unpack_double()
        ##rmsd = self.up.unpack_double()

        ##frame.append([en, avg, rmsd])
        ##else:
        # frame.append([en, en, 0.0])
        # except Exception as e:
        # print("Error in unpacking ",e)
        # break

        return frame


# NOTE: We are adding the default handlers at the end of the file
_default_handlers = [
    [EdrIO, 'edr', '.edr']
]

_handler_map = {}
_extensions_map = {}


def add_default_handler(ioclass, format, extension=None):
    """Register a new data handler for a given format in
       the default handler list.

       This is a convenience function used internally to setup the
       default handlers. It can be used to add other handlers at
       runtime even if this isn't a suggested practice.

       **Parameters**

       ioclass: IOHandler subclass
       format: str
         A string identifier representing the format
       extension: str, optional
         The file extension associated with the format.

    """
    if format in _handler_map:
        print("Warning: format {} already present.".format(format))

    _handler_map[format] = ioclass

    if extension in _extensions_map:
        print("Warning: extension {} already handled by {} handler."
              .format(extension, _extensions_map[extension]))

    if extension is not None:
        _extensions_map[extension] = format


# Registering the default handlers
for h in _default_handlers:
    add_default_handler(*h)


## We add also the cclib handlers
# load_cclib = False
# try:
# import cclib
# load_cclib = True
# except ImportError:
# print('cclib not found. Install cclib for more handlers.')

# if load_cclib:
# from .handlers._cclib import _cclib_handlers
# for hclass, format in _cclib_handlers:
# add_default_handler(hclass, format)

def get_handler_class(ext):
    """Get the IOHandler that can handle the extension *ext*."""

    if ext in _extensions_map:
        format = _extensions_map[ext]
    else:
        raise ValueError("Unknown format for %s extension." % ext)

    if format in _handler_map:
        hc = _handler_map[format]
        return hc
    else:
        matches = difflib.get_close_matches(format, _handler_map.keys())
        raise ValueError("Unknown Handler for format %s, close matches: %s"
                         % (format, str(matches)))


def datafile(filename, mode="rb", format=None):
    """Initialize the appropriate
    :py:class:`~chemlab.io.iohandler.IOHandler` for a given file
    extension or file format.

    The *datafile* function can be conveniently used to quickly read
    or write data in a certain format::

        >>> handler = datafile("molecule.pdb")
        >>> mol = handler.read("molecule")
        # You can also use this shortcut
        >>> mol = datafile("molecule.pdb").read("molecule")

    **Parameters**

    filename: str
          Path of the file to open.
    format: str or None
          When different from *None*, can be used to specify a
          format identifier for that file. It should be used when
          the extension is ambiguous or when there isn't a specified
          filename. See below for a list of the formats supported by chemlab.

    """

    filename = os.path.expanduser(filename)
    base, ext = os.path.splitext(filename)

    if format is None:
        hc = get_handler_class(ext)
    else:
        hc = _handler_map.get(format)
        if hc is None:
            raise ValueError('Format {} not supported.'.format(format))

    fd = open(filename, mode)

    handler = hc(fd)
    return handler

##filename = 'full_ener.edr' #Problems
# filename = 'md_2_1.edr' #Problems

##filename = 'md_3_1.edr' #Problems

##filename = 'em.edr' #Problems
# test =  EdrIO(filename, 'float') #datafile(filename)# .read('avail quantities')



# props = test.read('avail quantities')

# print('props ', props)



# for energy  in props:
# print('Parameter Name ',energy)
# final_data = test.read('quantity', energy)
# print(final_data)
# print('-----------------------------')


# time, LJ = datafile(filename).read('quantity', 'LJ (SR)')
# print('time is ',time)
# print('LJ is ', LJ)

# time, temp = datafile(filename).read('quantity', 'Temperature')
# print('time ',time)
# print('temp ', temp)
