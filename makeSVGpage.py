import  SVGStock as SVGS

import glob
import sys
if len(sys.argv)>2:
    if (sys.argv[1])!="":
        IBDList=sys.argv[1]
        path=sys.argv[2]
    else:
        print("yo")
else:
    print("error, see usage")
    exit 

print(IBDList)
print(path)

filelist=sorted(glob.glob(path+IBDList+"_*.svg"))
print(filelist)
buffer="<html><body>"
for item in filelist:
    data=SVGS.SVGStock(item,path)
    #print(data.getSvgImgLink())
    #print(data.getYahoo2YrLogChartLink())
    #print(data.getYahooProfileLink())
    #print(data.getYahooKeyStatisticsLink())

    buffer+="<div>"+data.getSvgImgLink()+"</div><div>"+data.getYahoo2YrLogChartLink()+" "+data.getYahooProfileLink()+" "+data.getYahooKeyStatisticsLink()+"</div>"
    
buffer+="</body></html>"
filename=IBDList+".html"
f=open(filename,'w')
f.write(buffer)
