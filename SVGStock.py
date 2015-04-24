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
        return '<a href="http://finance.yahoo.com/echarts?s='+self.ticker+'+Interactive#{%22range%22%3A%222y%22%2C%22scale%22%3A%22logarithmic%22comparisons%22%3A%7B%22%5EGSPC%22%3A%7B%22color%22%3A%22%23cc0000%22%2C%22weight%22%3A1%7D%2C%22%5EDJI%22%3A%7B%22color%22%3A%22%23009999%22%2C%22weight%22%3A1%7D%2C%22%5EIXIC%22%3A%7B%22color%22%3A%22%23ff00ff%22%2C%22weight%22%3A1%7D%7D%7D}">'+self.ticker.upper()+" 2yr Log Chart</a>"
    def getTicker(self):
        return self.ticker
    def getSvgImgLink(self):
        return '<img src="'+self.svgFile+'">' 
