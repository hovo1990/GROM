# -*- coding: utf-8 -*-
"""
    GROM.PDB_parse
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""


def cleanVal(val):
    tempus = val.split(' ')
    #print tempus
    for i in tempus:
        if i == '':
            pass
        else:
            return i

def PDBparse(filename):
    inFile = open(filename, 'r')
    try:
        final_list = []
        info = ''
        for line in inFile:
            #print line[0:7]
            temp = []
            if cleanVal(line[0:7]) == 'ATOM' or cleanVal(line[0:7]) == 'HETATM':
                temp.append(cleanVal(line[0:7])) #Record name
                temp.append(cleanVal(line[7:12])) #Atom serial number
                temp.append(cleanVal(line[13:17])) #Atom name
                temp.append(cleanVal(line[17:21])) #Residue name
                temp.append(cleanVal(line[21:23])) #Chain identifier
                temp.append(cleanVal(line[23:27])) #Residue sequence number
                temp.append(cleanVal(line[31:39])) #Orthogonal coordinates for X in Angstroms
                temp.append(cleanVal(line[39:47])) #Orthogonal coordinates for Y in Angstroms
                temp.append(cleanVal(line[47:55])) #Orthogonal coordinates for Z in Angstroms
                temp.append(cleanVal(line[55:61])) #Occupancy
                temp.append(cleanVal(line[61:67])) #Temperature factor
                temp.append(cleanVal(line[77:79])) #Element symbol, right-justified.
                temp.append(cleanVal(line[78:81])) #Element symbol, right-justified.
                #print temp
                if temp[-1] == '\n':
                    final_list.append(temp[:-1])
                else:
                    final_list.append(temp)
            else:
                info += line
        return final_list,info
    except:
        print('Oh come on  PDB parse problem')


def make_info(info_list):
    text = ''
    for i in info_list:
        for j in i:
            text += j + ' '
        text += '\n'
    return text



def write_SingleLine_to_PDB(open_file,line,info = None):
    exception = None
    fh = open_file
    s = ''
    try:
        s = str(line[0]) + '{:>7}'.format(line[1])
        if len(line[2]) < 4:
            s  +=  2*' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
        else:
            #print 'line[2] ',line[2]
            s  += ' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
        s += '{:>2}'.format(line[4]) + '{:>4}'.format(line[5])
        s += '{:>12}'.format(line[6]) + '{:>8}'.format(line[7]) + '{:>8}'.format(line[8])
        s += '{:>6}'.format(line[9]) + '{:>6}'.format(line[10]) #+ '{:>12}'.format(line[12])
        s += 11*' '
        if "\n" not in line[11]:
            line[11] += '\n'
        s +=  '{:<2}'.format(line[11])
        fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        #if fh is not None:
            #fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ",exception)



def write_to_PDB(data,to_save,info = None,):
    exception = None
    fh = open(to_save,'w')
    s = ''
    try:
        print('Oh come on')
        for line in data:
        #print line
            s = str(line[0]) + '{:>7}'.format(line[1])
            if len(line[2]) < 4:
                s  +=  2*' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
            else:
                #print 'line[2] ',line[2]
                s  += ' ' + '{:<3}'.format(line[2]) + '{:>4}'.format(line[3])
            s += '{:>2}'.format(line[4]) + '{:>4}'.format(line[5])
            s += '{:>12}'.format(line[6]) + '{:>8}'.format(line[7]) + '{:>8}'.format(line[8])
            s += '{:>6}'.format(line[9]) + '{:>6}'.format(line[10]) #+ '{:>12}'.format(line[12])
            #last_elem = ''
            #print 'line[12] is ',line[12]
            #print 'length is ',len(line)
            #last_elem = helper_function(line,11)
            #print 'last elem is ',last_elem
            s += 11*' '
            s +=  '{:<2}'.format(line[11])
            s += '\n'
            fh.write(s)
    except EnvironmentError as e:
        exception = e
    finally:
        if fh is not None:
            fh.close()
        if exception is not None:
            raise exception
            print("Yikes there is a problem ",exception)

#filename = "1IYX.pdb"


#mol,info = PDBparse(filename)
#print mol
#print info
##print info
##print '\n'
##print '--'*20
##print mol

#text = make_info(info)
#print text