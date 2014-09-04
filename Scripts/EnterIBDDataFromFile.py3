#!/usr/bin/env/python 
# -*- python -*-


"""
"""

import sys #for cmd line arguments

def read_file(myfile):
    """
    """
    for line in myfile:
        """ if this is a blank line, reset our counter """
        if line.strip():
            splitline=line.split(',')
            #print(splitline)
            if splitline[0]=="8585":
                #print("8585")
                #EightyFiveFilename="../Data/8585.txt2"
                filename="../Data/8585.txt"
            if splitline[0]=="Top200":
                #print("200")
                #Top200Filename="../Data/Top200Composite.txt2"
                filename="../Data/Top200Composite.txt"
            if splitline[0]=="BC20":
                #print("20")
                #BC20Filename="../Data/BC20.txt2"
                filename="../Data/BC20.txt"
            if splitline[0]=="IBD50":
                #print("50")
                #IBD50Filename="../Data/IBD50.txt2"
                filename="../Data/IBD50.txt"
            print("Writing %s data to %s." % (splitline[0],filename))
            file_prepend_write(filename,splitline)

#end def read_file

def file_prepend_write(filename,data):
    """
    This function takes a filename and a list 
    The list is written to the beginning of the file
    The list has three elements. data[0]= investment list, data[1]= date, data[2]= stock list
    """
    with open(filename,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(data[1] + '\n' + data[2] + '\n' + content)
        f.close

def usage():
    print("This program reads the data saved off from IBD pdfs and processed by IBDPDFExtractor and writes the data to the appropriate datat file.")
    sys.exit('Usage: %s inputfilename.ext' % __file__)
#    sys.exit('Usage: %s inputfilename.ext' % sys.argv[0])

"""
-----------------------------------------------
MAIN
-----------------------------------------------
"""
#print(len(sys.argv))
if (len(sys.argv) == 2):
    data_file_handler = open(sys.argv[1])
    read_file(data_file_handler)
    data_file_handler.close()
else:
    usage()


