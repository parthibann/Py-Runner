# Usage :
# This module contains a class "googleChart" which is used to form source code of charts.
# It makes only the chart source and not the entire HTML source, so it has to be wrapped with the HTML source as following.
# HTML Sample Source :
#        <html>
#        <head>
#        <script type="text/javascript" src="https://www.google.com/jsapi"></script> 
#------- Here is the place where you want to call the getChart function from googleChart class to get the chart source.
#------- (e.g) a = googleChart()
#------- a.getChart("PieChart","['Result', 'Total'],['Pass',11],['Fail',7]","test","colors: ['green','red']")
#        </head>
#        <body>
#------- the title used for creating charts only has to used for the div id.
#        <div id="titleUsedForChart" style="width: 900px; height: 500px;"></div>
#        </body>
#        </html>

class googleChart():
    """
    This will make pie-charts and column-charts using google api.
    """

    def getChart(self,chartType,data,title,colors=None):
        """
        It will make the entire pie-chart HTML source and return it.
        ARGS :
		ARG 1 - > chartType is mandatory argument
		chartType can be either "PieChart" or "BarChart"
		ARG 2 -> data is mandatoy argument
		Input for data has to be given in this format : "['Result', 'Total'],['Pass',11],['Fail',7]"
		ARG 3 - > title is mandatory argument
		title can be any string that represents the chart.
		ARG 4 - > colors is an optional argument
		Input for colours has to be given in this format : "colors: ['green','red']"
		"""
        part1="""
        <script type="text/javascript">
        google.load("visualization", "1", {packages:["corechart"]});
        google.setOnLoadCallback(drawChart);
        function drawChart() {
        var data = google.visualization.arrayToDataTable([
        """+data+"""
        ]);
        var options = {
        title: '"""+title+"""'"""
        if colors==None:
            _colors=""
        else:
            _colors=","+colors
        part2=_colors+"""};
        var chart = new google.visualization."""+chartType+"""(document.getElementById('"""+title+"""'));
        chart.draw(data, options);
        }
        </script>
        """
        return part1+part2
	
#------------------------------------------------------------------------------------------------------------
import os
import sys

class makeStatisticsReport():
    """
    This is used to make the statistics html report.
    """
    def __init__(self,_dir):
        """
        Initializing global variables.
        """
        self.dir=_dir
        self.gchart=googleChart()

    def getHTMLFileNames(self):
        """
        To get the list of files with .html or .htm extension and return it.
        """
        HTMLFiles = []
        for _file in os.listdir(self.dir):
            if _file.lower().endswith(".html"):
                HTMLFiles.append(_file)
            elif _file.lower().endswith(".htm"):
                HTMLFiles.append(_file)
        return HTMLFiles

    def getStatisticsFromHTMLTestOutput(self):
        """
        To get the statistics from each testsuite report and return it as json object.
        """
        _resultData = ""
        _outputFiles = self.getHTMLFileNames()
        for file in _outputFiles:
            filename = "{"+file[:-5]+":"
            file = self.dir+"/"+file
            _resultData=_resultData+str(filename)
            with open(file) as infile:
                copy = False
                for line in infile:
                    if line.strip()=="<tr id='total_row'>":
                        copy=True
                    elif line.strip() == "<td>&nbsp;</td>":
                        copy=False
                    elif copy:
                        _line = (str(line).replace('    <td>','')).rstrip('\r\n')
                        _replaceLine = str(_line).replace('</td>',':')
                        _resultData=_resultData+_replaceLine
            _resultData=_resultData+"},"
        return _resultData
                        
    def getTotalPassed(self):
        """
        To get the total passed test cases.
        """
        _totalPassed = 0
        statistics = self.getStatisticsFromHTMLTestOutput()
        _suiteStats=statistics.split(',')
        for suite in _suiteStats:
            if suite.count(':')==6:
			    _totalPassed = _totalPassed + int(suite.split(':')[3])
        return _totalPassed

    def getTotalFailed(self):
        """
		To get the total failed test cases.
        """
        _totalFailed = 0
        statistics = self.getStatisticsFromHTMLTestOutput()
        _suiteStats=statistics.split(',')
        for suite in _suiteStats:
            if suite.count(':')==6:
			    _totalFailed = _totalFailed + int(suite.split(':')[4])
        return _totalFailed

    def getOverallStatistics(self):
        """
        To make overall statistics.
        """
        _totalPassed = self.getTotalPassed()
        _totalFailed = self.getTotalFailed()
        _details = "['Result', 'Total'],['Pass',"+str(_totalPassed)+"],['Fail',"+str(_totalFailed)+"]"
        return _details		

    def getTestCoverageStatistics(self):
        """
        To get the test coverage statistics.
        """
        _data = "['Suite Name', 'Total Test Cases'],"
        statistics = self.getStatisticsFromHTMLTestOutput()
        _suiteStats=statistics.split(',')
        for suite in _suiteStats:
            if suite.count(':')==6:
                _suiteDetails = suite.split(':')
                _suiteName = _suiteDetails[0][1:]
                _total = _suiteDetails[2]
                _data = _data+"['"+_suiteName+"',"+_total+"],"
        return _data[:-1]
		
    def getInduvidualTestSuiteStatistics(self):
        """
        To get each and every individual test suite statistics.
        """
        _details = "['Suite Name', 'Pass', 'Fail'],"
        statistics = self.getStatisticsFromHTMLTestOutput()
        _suiteStats=statistics.split(',')
        for suite in _suiteStats:
            if suite.count(':')==6:
                _suiteDetails = suite.split(':')
                _suiteName = _suiteDetails[0][1:]
                _passed = _suiteDetails[3]
                _failed = _suiteDetails[4]
                _details = _details + "['"+_suiteName+"',"+_passed+","+_failed+"],"
        return _details[:-1]

    def getOverallStatisticsHTML(self):
        """
        This will make the overall statistics html page.
        """
        chartType = "PieChart"
        data = self.getOverallStatistics()
        overallStatisticsTitle = "Overall Statistics"
        colors = "colors: ['green','red']"
        script = self.gchart.getChart(chartType,data,overallStatisticsTitle,colors)
        return script
		
    def getTestCoverageStatisticsHTML(self):
        """
        This will make the test coverage statistics html page.
        """
        chartType = "PieChart"
        data = self.getTestCoverageStatistics()
        title = "Test Coverage Statistics"
        script = self.gchart.getChart(chartType,data,title)
        return script
		
    def getInduvidualTestSuiteStatisticsHTML(self):
        """
        This will make Individual Test Suite Statistics HTML page.
        """
        chartType = "BarChart"
        data = self.getInduvidualTestSuiteStatistics()
        testSuiteStatisticsTitle = "Test Suite Statistics"
        colors = "colors: ['green','red']"
        script = self.gchart.getChart(chartType,data,testSuiteStatisticsTitle,colors)
        return script		
		
    def deleteStatisticsFileIfExists(self):
	"""
	To delete the Statistics.html file if it is already exists in the mentioned directory.
	"""
	try:
	    os.remove(self.dir+'/Statistics.html')
	except OSError:
	    pass
		
    def getStatisticsReport(self):
        """
        This method will create the source of statistics.html page and return it.
        """
        self.deleteStatisticsFileIfExists()
        pageSource="""
        <html>
        <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        """+self.getOverallStatisticsHTML()+self.getTestCoverageStatisticsHTML()+self.getInduvidualTestSuiteStatisticsHTML()+"""
        </head>
        <body>
        <div id="Overall Statistics" style="width: 900px; height: 600px;"></div>
        <div id="Test Coverage Statistics" style="width: 900px; height: 600px;"></div>
        <div id="Test Suite Statistics" style="width: 900px; height: 600px;"></div>
        """
        f = open(self.dir+'/Statistics.html','w')
        f.write(pageSource)
        f.close
		
def main(argv):
    if len(argv)<=1:
        print "please enter folder name."
    elif len(argv)==2:
        a = makeStatisticsReport(str(argv[1]))
        a.getStatisticsReport()
		
if __name__ == '__main__':
    main(sys.argv)
