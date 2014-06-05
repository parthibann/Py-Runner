# -- Config Settings :
_serverIpAddress = 'localhost'
_port = '1905'
_testlinkURL = 'http://localhost/testlink/lib/api/xmlrpc/v1/xmlrpc.php'

#-----------------------------------------------------------------------------------------------------------------------
#------------------------------ SelectTests Template -------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
import unittest
import TestManager

class SelectTestCasesHTMLMaker():
    """
    This class will take the list of testcases which is returned from TestManager.py and transforms it into html page which will allow the user to select test cases to run.
    """
    def __init__(self,_theme='skyblue'):
        """
        Initializing global variables.
        """
        self.listOfTestSuites = TestManager.TestManager().TestSuites()
        self.theme = _theme
        self.serverIpAddress = _serverIpAddress
        self.port = _port

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
        linksPart1 = "<input type=\"checkbox\" name=\""
        linksPart2 = "\" class=\""
        linksPart3 = "\"><a href=\"#"
        linksPart4 = "\">"
        linksPart5 = "</a><br>"
        testSuites = self.getTestSuiteNames()
        for suite in testSuites:
            link = linksPart1+suite+linksPart2+suite+linksPart3+suite+linksPart4+suite+linksPart5
            links = links+link
        return links

    def makeTestSuiteSelectionJquery(self):
        """
        To make individual test suite selection jquery
        """
        Jquery = ""
        part1 = "$('."
        part2 = "').click( function(){$('input[name="
        part3 = "]').prop('checked',$(this).is(':checked'));});"
        testSuites = self.getTestSuiteNames()
        for suite in testSuites:
            _jquery = part1+suite+part2+suite+part3
            Jquery = Jquery+_jquery
        return Jquery
                
    def makeTestSelectorHTML(self):
        """
        """
        HTMLPart1 = """
        <html>
        <head>
        <script src="http://code.jquery.com/jquery-1.9.1.js" type="text/javascript"></script>
        <script type="text/javascript">
            $(function () {
              $(".runnerRadio").click(function(){if($(this).val()==="TestLinkRunner") $("#TLRunner").show("fast"); else $("#TLRunner").hide("fast");})
              $('.RunSelectedTests').click( function(){
                var chkId = '';
                $('.chkTest:checked').each(function() {
                  chkId += $(this).val() + ",";
                });
                testCases = chkId;
		        var selectedRunner = $('input[name=testRunner]:radio:checked').val()
		        var userId = $('input:text[name=useridtxtbox]').val();
		        var testPlanId = $('input:text[name=testplantxtbox]').val();
		        var buildName = $('input:text[name=buildnametxtbox]').val();
                $.ajax({type:'POST',url:"http://"""+self.serverIpAddress+""":"""+self.port+"""/runtest",data : JSON.stringify({"testCases":testCases,"Runner":selectedRunner,"userId":userId,"testPlanId":testPlanId,"buildName":buildName}),dataType: "json",success:function(){alert('success')},error: function(e){alert(JSON.stringify(e))},contentType: "application/json; charset=utf-8"});
              });
              $('.selectAllTestCases').click( function(){
                $('.chkTest').prop('checked',$(this).is(':checked'));
              });"""+self.makeTestSuiteSelectionJquery()+"""
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
        <div id="TLRunner" style="background-color:"""+self.theme+""";font-weight:bold;text-align:center;width:100%;display:none;">User Id:
	    <input type="text" name="useridtxtbox" placeholder="Enter User Id *" size=14>TestPlan Id :
	    <input type="text" name="testplantxtbox" placeholder="Enter TestPlan Id *" size=14>Build Name :
	    <input type="text" name="buildnametxtbox" placeholder="Enter Build Name *" size=14></div>
        <div id="runner" style="background-color:"""+self.theme+""";font-weight:bold;text-align:center;width:100%;">Select Runner : 
        <input type="radio" name="testRunner" class="runnerRadio" value="HTMLTestRunner" checked>HTMLTestRunner
        <input type="radio" name="testRunner" class="runnerRadio" value="TestLinkRunner">TestLinkRunner
        <input type="checkbox" class="selectAllTestCases" />Select All Test Cases
        <button type="button" class="RunSelectedTests">Run</button></div>
        </div>
        </body>
        </html>
         """
         
        HTMLPage = (HTMLPart1+HTMLPart2+HTMLPart3+HTMLPart4+HTMLPart5)
        return HTMLPage

#-------------------------------------------------------------------------------------------------------------------------------------
from ExtLib import bottle
from ExtLib.bottle import route,run,request,response,static_file,error,redirect
from ExtLib import HTMLTestRunner
from ExtLib import HTMLIndexCreator
from ExtLib.TestLinkRunner import TestLinkRunner
import unittest
import os
import json

#---------------------------------------------------------------------------------------------------
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
    
#----------------------------------------------------------------------------------------------------
@route('/selecttests')
def selectTests():
    """
    It will return TestSelector Html page.
    """
    selectTestsHTMLFile = SelectTestCasesHTMLMaker().makeTestSelectorHTML()
    return selectTestsHTMLFile

#-----------------------------------------------------------------------------------------------------
@route('/results/')
@route('/results/:filename')
def results(filename='index.html'):
    """
    This will return the results of executed test cases, static html reports are served using this route.
    """
    _rootPath = os.path.abspath(os.path.dirname(__file__))
    return static_file(filename,root=_rootPath+'/Output')

#------------------------------------------------------------------------------------------------------
@route('/runtest',method=['POST','OPTIONS'])
@enable_cros
def runtest():
    """
    This method will run the testcases selected in TestSelector.html page
    """
    pwd = os.path.abspath(os.path.dirname(__file__))
    response = json.loads(request.body.read())
    testCases = (str(response['testCases'])).split(',')
    testCases.pop()
    _runner = (str(response['Runner']))
    _buildName = (str(response['buildName']))
    _userId = (str(response['userId']))
    _testPlanId = (str(response['testPlanId']))
    totalTestCases = len(testCases)
    if _runner == 'HTMLTestRunner':
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
    elif _runner == 'TestLinkRunner':
        _TLRunner = TestLinkRunner(_testlinkURL,_userId,_testPlanId,_buildName)
        if totalTestCases == 0:
            return "Select testcases to run.."
        else:
            suite = unittest.TestSuite()
            for testCase in testCases:
                _testSuiteName = ((str(testCase)).split(' ')[0])[1:]
                classObj = my_import(_testSuiteName)
                _testCaseName = ((((str(testCase)).split(' ')[1])[:-1]).split('='))[1]
                suite.addTest(classObj(_testCaseName))
            _TLRunner.run(suite)
        return "Test(s) complete....."


def my_import(importName):
    """
    Takes a class name as input and returns that class object.
    """
    className = importName.split('.')[-1]
    moduleName = importName[:-(len(className)+1)]
    mod = __import__(moduleName)
    components = moduleName.split('.')
    for comp in components[1:]:
        mod = getattr(mod,comp)
    class_ = getattr(mod,className)
    return class_

def getTestSuiteNames(testCases):
    """
    Returns unique testsuite names of the given testcases.
    """
    testSuites = []
    for testCase in testCases:
        testSuite = (str(testCase).split(' '))[0]
        testSuiteName = testSuite.split('.')[-1]
        testSuites.append(testSuiteName)
    return list(set(testSuites))

#-----------------------------------------------------------------------
@error(404)
def error404(error):
    """
    Returns the following contents for "Resource not found"
    """
    return '<strong><center><h3>The Resource you are looking for is currently not available or removed.</h3></center></strong>'

#------------------------------------------------------------------------        
run(host=_serverIpAddress,port=_port,debug=False)

