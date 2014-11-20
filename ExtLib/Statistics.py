import os
import sys

wd = os.path.abspath(os.path.dirname(__file__))
outputDir = wd+"/../Output/"

def deleteStatisticsFileIfExists(_outputDir=outputDir):
    """ """
    try:
        os.remove(_outputDir+'statistics.html')
    except OSError:
        pass

def getHtmlFileNames(_outputDir=outputDir):
    """ """
    deleteStatisticsFileIfExists(_outputDir)
    HTMLFiles = []
    for _file in os.listdir(_outputDir):
        if _file.lower().endswith(".html"):
            if _file.lower() == "index.html":
                pass
            else:
                HTMLFiles.append(_file)
        elif _file.lower().endswith(".htm"):
            if _file.lower() == "index.htm":
                pass
            else:
                HTMLFiles.append(_file)
    return HTMLFiles

def getStatisticsFromHtmlTestOutput(_outputDir=outputDir):
    """ """
    _stats = []
    _outputFiles = getHtmlFileNames(_outputDir)
    for file in _outputFiles:
        _file = _outputDir+file
        with open(_file) as infile:
            _Data = ""
            _Data =  str(file[:-5]) + "!~!"
            copy = False
            for line in infile:
                if line.strip()=="<tr id='total_row'>":
                    copy=True
                elif line.strip() == "<td>&nbsp;</td>":
                    copy=False
                elif copy:
                    _line = (str(line).replace('    <td>','')).rstrip('\r\n')
                    _replaceLine = str(_line).replace('</td>','!~!')
                    _Data=_Data + _replaceLine
            _stats.append(_Data)
    return _stats

class overviewReport():
    def __init__(self,projectName,_outputDir=outputDir):
        self.outputDir = _outputDir
        self.projectName = projectName
        self.reportData = getStatisticsFromHtmlTestOutput(self.outputDir)

    def getTotalPassed(self):
        """ """
        totalPassed = 0
        stats = self.reportData
        for stat in stats:
            passed = stat.split('!~!')[3]
            totalPassed = totalPassed + int(passed)
        return totalPassed

    def getTotalFailed(self):
        """ """
        totalFailed = 0
        stats = self.reportData
        for stat in stats:
            failed = stat.split('!~!')[4]
            totalFailed = totalFailed + int(failed)
        return totalFailed

    def getTotalError(self):
        """ """
        totalError = 0
        stats = self.reportData
        for stat in stats:
            error = stat.split('!~!')[5]
            totalError = totalError + int(error)
        return totalError

    def getTotalTestcases(self):
        """ """
        totalCases = 0
        stats = self.reportData
        for stat in stats:
            total = stat.split('!~!')[2]
            totalCases = totalCases + int(total)
        return totalCases

    def makeReport(self):
        """ """
        part1 = """
        <html>
        <head><title>Overview Report</title><head>
        <body>
        <table>
        <tr><td><b>Project Name</b></td><td>:
        """
        part2="""</td></tr>
        <tr><td><b>Language</b></td><td>: Python</td></tr>
        <tr><td><b>Framework</b></td><td>: Unittest </td></tr>
        </table>
        <p> The below are the overview of the automated testsuite / testcase results.
        <div class="statsDiv">
        <table id="stats">
        <thead>    
        <tr><th>Functionality</th><th>Total</th><th>Pass</th><th>Fail</th><th>Error</th></tr>
        </thead>
        """
        part3="""
        </table></div>
        </body>
        </html>
        <style>
        #stats{ background-color : #fff; color : #446bb3; border-collapse:collapse;}
        #stats thead { background-color: #446bb3  ; color : #fff; font: bold 14px verdana; padding:4px; line-height:30px}
        #stats tbody tr:nth-child(even) {background: #CCC;}
        #stats tbody tr:nth-child(odd) {background: #FFF}
        .statsDiv{display:inline-block;padding-top: 8px;padding-bottom: 10px;margin: 0 auto 20px auto;background-color: #446bb3;border-radius: 10px;-moz-border-radius: 10px;-webkit-border-radius: 10px;color: #446bb3;padding:10px;}    
        </style>
        """
        testResults = ""
        for stat in self.reportData:
            testData = stat.split('!~!')
            testName = testData[0]
            totalTestcase = testData[2]
            passed = testData[3]
            failed = testData[4]
            error = testData[5]
            htmlData = "<tr><td>"+testName+"</td><td>"+totalTestcase+"</td><td>"+passed+"</td><td>"+failed+"</td><td>"+error+"</td>"
            testResults = testResults + htmlData
        testResults = testResults + "<tr><td>Total</td><td>"+str(self.getTotalTestcases())+"</td><td>"+str(self.getTotalPassed())+"</td><td>"+str(self.getTotalFailed())+"</td><td>"+str(self.getTotalError())+"</td>"
        page = part1 +self.projectName + part2 + testResults + part3
        f = open(outputDir+'statistics.html','w')
        f.write(page)
        f.close

def main(argv):
    if len(argv)<=1:
        print "Usage:"
        print "Python Statistics.py <project name> <output dir (optional)>"
    elif len(argv)==2:
        a = overviewReport(str(argv[1]))
        a.makeReport()
    elif len(argv)==3:
        a = overviewReport(str(argv[1]),str(argv[2]))
        a.makeReport()

if __name__ == '__main__':
    main(sys.argv)
