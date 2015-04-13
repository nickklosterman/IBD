class SVGStock:
    def __init__(self,svgFile):
        self.ticker=(svgFile.split('_'))[1]
        self.IBDList=(svgFile.split('_'))[0]
        self.svgFile=svgFile
        
    def getYahooKeyStatisticsLink(self):
        return '<a href="http://finance.yahoo.com/q/ks?s='+self.ticker+'+Key+Statistics">'+self.ticker.upper()+' Key Statistics</a>'
    def getYahooProfileLink(self):
        return '<a href="http://finance.yahoo.com/q/pr?s='+self.ticker+'+Profile">'+self.ticker.upper()+' Profile</a>'
    def getYahoo2YrLogChartLink(self):
        return '<a href="http://finance.yahoo.com/echarts?s='+self.ticker+'+Interactive#{%22range%22%3A%222y%22%2C%22scale%22%3A%22logarithmic%22}">'+self.ticker.upper()+" 2yr Log Chart</a>"
    def getTicker(self):
        return self.ticker
    def getSvgImgLink(self):
        return '<img src="'+self.svgFile+'">' 
