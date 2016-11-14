# -*- coding: utf-8 -*-
"""
    GROM.Gro_parse
    ~~~~~~~~~~~~~

    This is for parsing gro format file

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import sys


def separate_vals(val):
    tempNum = ''
    tempName = ''
    # print('val is ',val)
    for i in val:
        try:
            temp = int(i)
            tempNum += i
            # test = float(tempNum)
        except:
            tempName += i
    return tempNum, tempName
    # except Exception as e:
    # print("Error in separate_vals is ",e)
    # sys.exit(0)


def cleanVal(line):
    try:
        tempus = line.split(' ')
        # print tempus
        fixed_line = []
        for i in range(len(tempus)):
            if tempus[i] == '':
                pass
            elif '\n' in tempus[i]:
                fixed_line.append(tempus[i][:-1])
            else:
                if len(fixed_line) == 0:
                    residNum, residName = separate_vals(tempus[i])
                    if len(residNum) == 0:
                        fixed_line.append(residName)
                    elif len(residName) == 0:
                        fixed_line.append(residNum)
                    else:
                        fixed_line.append(residNum)
                        fixed_line.append(residName)
                else:
                    fixed_line.append(tempus[i])
        return fixed_line
    except Exception as e:
        print("Error in cleanVal is ", e)
        sys.exit(0)


def groParse(filename):
    inFile = open(filename, 'r')
    try:
        final_list = []
        for line in inFile:
            temp = cleanVal(line)
            # print('temp is ',temp)
            final_list.append(tuple(temp))
        return final_list
    except Exception as e:
        print('Problem with gro Parse: ', e)
    finally:
        inFile.close()


        # filename  = 'conf.gro'
        # mol= groParse(filename)
        # print('mol is ',mol)

        # y = mol[-2]
        # print('y is ',y)
        ##x = "%5d%-5s%5s%5d%8.3f%8.3f    %8.3f%8.4f%8.4f%8.4f" %(y[0],y[1],int(y[2]),
        ##float(y[3]),float(y[4]),float(y[5]))


##print(x)

# x1 = '%10s%5s%5d%8.4f%8.4f%8.4f\n' %(y[0],y[1],int(y[2]),float(y[3]),float(y[4]),float(y[5]))
# print('x1 is ',x1)
# print(len(x1))


def write_extraData_to_GRO(open_file, line, info=None):
    exception = None
    fh = open_file
    s = ' '
    try:
        for i in line:
            s += i + ' '
        s += '\n'
        fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        # if fh is not None:
        # fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ", exception)


def write_vectorBox_to_GRO(open_file, line, info=None):
    exception = None
    fh = open_file
    s = ' '
    try:
        for i in range(3):
            s += line[-1] + ' '
        s += '\n'
        fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        # if fh is not None:
        # fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ", exception)


def write_SingleLine_to_GRO(open_file, line, info=None):
    exception = None
    fh = open_file
    s = ''
    try:
        s = '{:>5}'.format(line[0])
        s += '{:<5}'.format(line[1]) + '{:>5}'.format(line[2])
        s += '{:>5}'.format(line[3]) + '{:>8}'.format(line[4]) + '{:>8}'.format(line[5])
        # s += '{:>8}'.format(line[6])
        # s += 11*' '
        if "\n" not in line[6]:
            line[6] += '\n'
        s += '{:>8}'.format(line[6])
        fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        # if fh is not None:
        # fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ", exception)


def write_to_PDB(data, to_save, info=None, ):
    exception = None
    fh = open(to_save, 'w')
    s = ''
    try:
        print('Oh come on')
        for line in data:
            # print line
            s = str(line[0]) + '{:>7}'.format(line[1])
            if len(line[2]) < 4:
                s += 2 * ' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
            else:
                # print 'line[2] ',line[2]
                s += ' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
            s += '{:>2}'.format(line[4]) + '{:>4}'.format(line[5])
            s += '{:>12}'.format(line[6]) + '{:>8}'.format(line[7]) + '{:>8}'.format(line[8])
            s += '{:>6}'.format(line[9]) + '{:>6}'.format(line[10])  # + '{:>12}'.format(line[12])
            # last_elem = ''
            # print 'line[12] is ',line[12]
            # print 'length is ',len(line)
            # last_elem = helper_function(line,11)
            # print 'last elem is ',last_elem
            s += 11 * ' '
            s += '{:<2}'.format(line[11])
            s += '\n'
            fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        if fh is not None:
            fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ", exception)

            # filename = "1IYX.pdb"


            # mol,info = PDBparse(filename)
            # print mol
            # print info
            ##print info
            ##print '\n'
            ##print '--'*20
            ##print mol

            # text = make_info(info)
            # print text
