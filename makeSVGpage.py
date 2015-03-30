import  SVGStock as SVGS

import glob
import sys
if len(sys.argv)>1:
    if (sys.argv[1])!="":
        IBDList=sys.argv[1]
else:
    print("error")
    exit 
        
filelist=sorted(glob.glob(IBDList+"_*.svg"))
buffer="<html><body>"
for item in filelist:
    data=SVGS.SVGStock(item)
    #print(data.getSvgImgLink())
    #print(data.getYahoo2YrLogChartLink())
    #print(data.getYahooProfileLink())
    #print(data.getYahooKeyStatisticsLink())

    buffer+=data.getSvgImgLink()+" "+data.getYahoo2YrLogChartLink()+" "+data.getYahooProfileLink()+" "+data.getYahooKeyStatisticsLink()
buffer+="</body></html>"
filename=IBDList+".html"
f=open(filename,'r+')
f.write(buffer)
