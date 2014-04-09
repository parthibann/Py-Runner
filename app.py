#-----------------------------------------------------------------------------------------------------------------------
#------------------------------ SelectTests Template --------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
import unittest
import TestManager
import socket

class SelectTestCasesHTMLMaker():
    """
    """
    def __init__(self,_theme='skyblue'):
        """
        """
        self.listOfTestSuites = TestManager.TestManager().TestSuites()
        self.theme = _theme
        #self.machineIpAddress = socket.gethostbyname(socket.gethostname()) #Enable this on windows environments
        self.machineIpAddress = '192.168.6.124'

             
    def makeTestCases(self):
        """
        To display test cases
        """
        chkboxPart1 = "<input type=\"checkbox\" name=\""
        chkboxPart2 = "\" value=\""
        chkboxPart3 = "\" class=\"chkTest\">"
        chkboxPart4 = "<br><hr>"
        testCases = ""
        for testSuite in self.listOfTestSuites:
            loadSuite = unittest.TestLoader().loadTestsFromTestCase(testSuite)
            totalTestCases = loadSuite.countTestCases()
            for test in range(totalTestCases):
                strTest = str(loadSuite._tests[test])
                _suiteName = strTest.split('.')[-1][0:-1]
                _testName = strTest.split(' ')[0]
                chkboxValue =  "<"+strTest.split(' ')[1][1:-1]+" testMethod="+_testName+">"
                testCaseName = chkboxPart1+_suiteName+chkboxPart2+chkboxValue+chkboxPart3+_testName+chkboxPart4
                if test == 0:
                    suiteLink = "<A NAME=\""+_suiteName+"\">"+_suiteName+"</A><br><hr>"
                else:
                    suiteLink = ""
                testCases = testCases + suiteLink + testCaseName
        return testCases
       
    def getTestSuiteNames(self):
        """
        To return the list of test sutie names
        """
        suiteName = []
        for testSuite in self.listOfTestSuites:
            loadSuite = unittest.TestLoader().loadTestsFromTestCase(testSuite)
            totalTestCases = loadSuite.countTestCases()
            for test in range(totalTestCases):
                strTest = str(loadSuite._tests[test])
                _className = strTest.split('.')[-1][0:-1] # to get the class name alone
                suiteName.append(_className) # appending the class name to suite name
        uniqueSuiteName = list(set(suiteName)) # to get unique testsuites
        return uniqueSuiteName
            
    def makeLinks(self):
        """
        To make test suite Links
        """
        links = ""
        linksPart1 = "<a href=\"#"
        linksPart2 = "\">"
        linksPart3 = "</a><br>"
        testSuites = self.getTestSuiteNames()
        for suite in testSuites:
            link = linksPart1+suite+linksPart2+suite+linksPart3
            links = links+link
        return links              
                
    def makeTestSelectorHTML(self):
        """
        """
        HTMLPart1 = """
        <html>
        <head>
        <script src="http://code.jquery.com/jquery-1.9.1.js" type="text/javascript"></script>
        <script type="text/javascript">
            $(function () {
              $('.RunSelectedTests').click( function(){
                var chkId = '';
                $('.chkTest:checked').each(function() {
                  chkId += $(this).val() + ",";
                });
                testCases = chkId;
                $.ajax({type:'POST',url:"http://"""+self.machineIpAddress+""":1903/runtest",data : JSON.stringify({"testCases":testCases}),dataType: "json",success:function(){alert('success')},error: function(e){alert(JSON.stringify(e))},contentType: "application/json; charset=utf-8"});
              });
              $('.selectAllTestCases').click( function(){
                $('.chkTest').prop('checked',$(this).is(':checked'));
              });
            });
        </script>
        </head>
        <body><title>Select TestCases</title>
        <div id="container" style="width:100%;text-align:center;border:5px solid black;border-radius:10px;">
        <div id="pageTitle" style="background-color:"""+self.theme+""";font-size:18pt;font-weight:bold;">Test Selector</div>
        
        <div id="whiteSpace" style="height:0.3%;"></div>
        
        <div id="testSuitesTitle" style="background-color:"""+self.theme+""";font-weight:bold;float:left;width:15%;">TestSuites</div>
        <div id="testcasesTitle" style="background-color:"""+self.theme+""";font-weight:bold;float:right;width:84.7%;">TestCases</div>
        
        <div id="testSuites" style="background-color:lightgrey;font-weight:bold;float:left;width:15%;text-align:left;height:92%;overflow:scroll;">"""

        HTMLPart2 = self.makeLinks()

        HTMLPart3 = """</div>
        <div id="testCases" style="background-color:white;font-weight:bold;float:right;width:84.7%;height:92%;text-align:left;overflow:scroll;">"""

        HTMLPart4 = self.makeTestCases()
        
        HTMLPart5 = """</div>
        <div id="runner" style="background-color:"""+self.theme+""";font-weight:bold;text-align:center;width:100%;">Select Runner : 
        <input type="radio" name="testRunner" value="HTMLTestRunner" checked>HTMLTestRunner
        <input type="radio" name="testRunner" value="TestLinkRunner">TestLinkRunner
        <input type="checkbox" class="selectAllTestCases" />Select All Test Cases
        <button type="button" class="RunSelectedTests">Run</button></div>
        </div>
        </body>
        </html>
         """
         
        HTMLPage = (HTMLPart1+HTMLPart2+HTMLPart3+HTMLPart4+HTMLPart5)
        return HTMLPage

#-------------------------------------------------------------------------------------------------------------------------------------
from ExtLib.bottle import bottle
from ExtLib.bottle.bottle import route,run,request,response,static_file
from ExtLib import HTMLTestRunner
from ExtLib import HTMLIndexCreator
import unittest
import os
import json

def enable_cros(fn):
    def _enable_cros(*args,**kwargs):
        """
        To enable cross platform support this method is used.
        """
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        if bottle.request.method!='OPTIONS':
            return fn(*args, **kwargs)
    return _enable_cros
    

@route('/ping')
def ping():
    return "<h2><b>I'm ready to test Monarch</h2></b>"

@route('/selecttests')
def selectTests():
    selectTestsHTMLFile = SelectTestCasesHTMLMaker().makeTestSelectorHTML()
    return selectTestsHTMLFile

@route('/results/:filename')
def results(filename):
    _rootPath = os.path.abspath(os.path.dirname(__file__))
    return static_file(filename,root=_rootPath+'/Output')

@route('/runtest',method=['POST','OPTIONS'])
@enable_cros
def runtest():
    pwd = os.path.abspath(os.path.dirname(__file__))
    response = json.loads(request.body.read())
    testCases = (str(response['testCases'])).split(',')
    testCases.pop()
    totalTestCases = len(testCases)
    if totalTestCases == 0:
        return "Select testcases to run.."
    else:
        listOfTestSuiteNames = getTestSuiteNames(testCases)
        for testSuite in listOfTestSuiteNames:
            suite = unittest.TestSuite()
            for testCase in testCases:
                testSuiteName = ((str(testCase).split(' '))[0]).split('.')[-1]
                if testSuite == testSuiteName:
                    _testSuiteName = ((str(testCase)).split(' ')[0])[1:]
                    classObj = my_import(_testSuiteName)
                    _testCaseName = ((((str(testCase)).split(' ')[1])[:-1]).split('='))[1]
                    suite.addTest(classObj(_testCaseName))
                    _testModuleName = testSuiteName#((str(testSuite).split(".")[-1])[0:-2])    
            _output = open(pwd+"/Output/"+_testModuleName+".html","w")
            HTMLRunner = HTMLTestRunner.HTMLTestRunner(stream=_output,title=_testModuleName,description="Test case's for the module "+_testModuleName)
            HTMLRunner.run(suite)
    IndexMaker = HTMLIndexCreator.HTMLIndexCreator(pwd+"/Output/")
    IndexMaker.makeHTMLIndexFile()    
    return "Test(s) complete....."


def my_import(importName):
    className = importName.split('.')[-1]
    moduleName = importName[:-(len(className)+1)]
    mod = __import__(moduleName)
    components = moduleName.split('.')
    for comp in components[1:]:
        mod = getattr(mod,comp)
    class_ = getattr(mod,className)
    return class_

def getTestSuiteNames(testCases):
    testSuites = []
    for testCase in testCases:
        testSuite = (str(testCase).split(' '))[0]
        testSuiteName = testSuite.split('.')[-1]
        testSuites.append(testSuiteName)
    return list(set(testSuites))
        

run(host='192.168.6.124',port=1903,debug=False)

