#!/usr/bin/env/python3 
# -*- python -*-


"""
This program reads the data saved off from IBD pdfs and processed by IBDPDFExtractor and writes the data to the appropriate data file.
This data is read from /tmp/YYYY-MM-DD_IBDDataSorted.txt
The --test option will not write the results to the files.

The data is always added to the very beginning of each file. 
"""

import sys,datetime #for cmd line arguments

def read_file(myfile,testFlag):
    """
    """
    for line in myfile:
        okToWriteFlag=False
        """ if this is a blank line, reset our counter """
        if line.strip():
            splitline=line.split(',')
            #print(splitline)
            #print(len(splitline))
            year, month, day = (int(x) for x in splitline[1].split('-'))


#            date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. For example, date(2002, 12, 4).weekday() == 2, a Wednesday. See also isoweekday().
#            date.isoweekday() Return the day of the week as an integer, where Monday is 1 and Sunday is 7. For example, date(2002, 12, 4).isoweekday() == 3, a Wednesday. See also weekday(), isocalendar().
            
            dayOfWeek = datetime.date(year,month,day).weekday()
            #print("%i day of week" % dayOfWeek)
            
            if splitline[0]=="":
                print("Error in this file. It is missing the initial field.")
                break;
            if splitline[0]=="Unknown":
                if dayOfWeek==0 or dayOfWeek==2:
                    bestGuess="IBD50"
                elif dayOfWeek==1:
                    bestGuess="BC20"
                elif dayOfWeek==3:
                    bestGuess="Top200"
                elif dayOfWeek==4:
                    bestGuess="8585"

            if splitline[0]=="8585":
                if dayOfWeek != 4:
                    print("Date mismatch for 8585. Was expecting 4 but saw %i" % dayOfWeek)
                    
                #print("8585")
                #EightyFiveFilename="../Data/8585.txt2"
                if len(splitline[2].strip().split(' '))>65: #the lowest I've seen is 65 (for wk of Oct 17 2014, but we'll keep 75 as our threshold; #uggh just saw 72, so putting down to 65
                    okToWriteFlag=True
                    print("%s 8585 records on %s" % (len(splitline[2].strip().split(' ')),splitline[1]) )
                else:
                    print("8585 data length error. Less than 75 records")
                    print("Date:%s,Length:%s, last element: %s" % (splitline[1],len(splitline[2].strip().split(' ')), (splitline[2].strip().split(' '))[19]) )
                filename="../Data/8585.txt"
            if splitline[0]=="Top200":
                if dayOfWeek != 3:
                    print("Date mismatch for Top200. Was expecting 3 but saw %i" % dayOfWeek)
                #print("200")
                #Top200Filename="../Data/Top200Composite.txt2"
                if len(splitline[2].strip().split(' '))==200:
                    okToWriteFlag=True
                    #print("Top200 is 200 long")
                else:
                    print("Top 200 data length error. Not 200 records")
                    #print("Date:%s,Length:%s, last element: %s" % (splitline[1],len(splitline[2].strip().split(' ')), (splitline[2].strip().split(' '))[19]) )
                    print("Date:%s,Length:%s" % (splitline[1],len(splitline[2].strip().split(' ')) ))
                filename="../Data/Top200Composite.txt"
            if splitline[0]=="BC20":
                if dayOfWeek != 1:
                    print("Date mismatch for BC200. Was expecting 1 but saw %i" % dayOfWeek)
                #print("20")
                #BC20Filename="../Data/BC20.txt2"
                if len(splitline[2].strip().split(' '))==20:
                    okToWriteFlag=True
                    #print("BC20 is 20 long")
                else:
                    print("BC20 data length error.")
                    print("Only %s records. " % len(splitline[2].strip().split(' ')))
                    #print("Date:%s,Length:%s, last element: %s" % (splitline[1],len(splitline[2].strip().split(' ')), (splitline[2].strip().split(' '))[19]) )
                    print("Date:%s,Length:%s" % (splitline[1],len(splitline[2].strip().split(' ')) ))
                    #print((splitline[2].strip().split(' '))[19])
                filename="../Data/BC20.txt"
            if splitline[0]=="IBD50":
                if dayOfWeek != 0 and dayOfWeek != 2:
                    print("Date mismatch for IBD50. Was expecting 0 or 2 but saw %i" % dayOfWeek)
                #print("50")
                #IBD50Filename="../Data/IBD50.txt2"
                filename="../Data/IBD50.txt"
                if len(splitline[2].strip().split(' '))==50:
                    okToWriteFlag=True
                    #print("IBD50 is 50 long")
                else:
                    print("IBD50 data length error.")
                    print("Date:%s,Length:%s, last element: %s" % (splitline[1],len(splitline[2].strip().split(' ')), (splitline[2].strip().split(' '))[19]) )
                    #print((splitline[2].strip().split(' '))[19])
#            if okToWriteFlag==False:
#                print("Hmm looks like there is a date / data type mismatch.")
            if okToWriteFlag==True and not testFlag==True:
                file_prepend_write(filename,splitline)
            if testFlag==True:
                print("Data ok for %s on %s" % (splitline[0], splitline[1]))

#end def read_file

def file_prepend_write(filename,data):
    """
    This function takes a filename and a list 
    The list is written to the beginning of the file
    The list has three elements. data[0]= investment list, data[1]= date, data[2]= stock list

    A check is performed to prevent writing duplicate data out
    """
    entryExists=exists_in_file(filename,data)
    if (entryExists==False):
        print("Writing %s data from %s to %s." % (data[0],data[1],filename))
        with open(filename,'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(data[1] + '\n' + data[2] + '\n' + content)
            f.close
    else:
        print("Error: Write failed. Data for %s on %s is already present in %s." % (data[0],data[1],filename))

def exists_in_file(filename,data):
    """
    Check to see if an entry already exists in the file.
    Key off of the date.
    http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

    This method is a bit overkill. A naive solution is to go through the first ~20 lines and only search there. I'm really just trying to prevent multiple entries after I've already done it once and am still playing with the data.
    This however is a good method for compeleteness sake if I ever needed to recreate from all source files. God willing that will never happen.
    """
    import mmap
    f = open(filename)
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    searchstring=data[1] #key off of the date. the stock list could be repeated and cause false positives.
    b_searchstring = searchstring.encode('utf-8') #need it to be a bytearray in python3    http://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    if s.find(b_searchstring) != -1:
        return True
    else:
        return False
    
        
def usage():
    print("This program reads the data saved off from IBD pdfs and processed by IBDPDFExtractor and writes the data to the appropriate data file.")
    print("The --test option will not write the results to the files.")
    sys.exit('Usage: %s inputfilename.ext --inputfile=somefile [--test]' % __file__)
#    sys.exit('Usage: %s inputfilename.ext' % sys.argv[0])

"""
-----------------------------------------------
MAIN
-----------------------------------------------
"""
import getopt
testFlag=False
if (len(sys.argv) == 2 or len(sys.argv) == 3):
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:t', ['inputfile=',
                                                                     'test'
                                                                 ])
    except getopt.GetoptError as err:
        print( str(err)) # will print something like "option -a not recognized"                                         
        usage()                                                                                                  
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-i', '--inputfile'):
            inputfile=arg
        elif opt in ('-t', '--test'):
            testFlag=True
        else:
            assert False, "unhandled option"

    #print(len(sys.argv))
    # if (len(sys.argv) == 2):
    #     data_file_handler = open(inputfile)
    #     read_file(data_file_handler)
    #     data_file_handler.close()

    data_file_handler = open(inputfile)
    read_file(data_file_handler,testFlag)
    data_file_handler.close()

else:
    usage()


