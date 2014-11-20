# -- Config Settings :
_serverIpAddress = '127.0.0.1'
_port = '1904'
_testlinkURL = 'http://localhost/testlink/lib/api/xmlrpc/v1/xmlrpc.php'         

#--------------------------------------------------------------------------------------------------
from ExtLib import bottle
from ExtLib.bottle import route,run,request,response,static_file,error,template
from ExtLib import HTMLTestRunner
from ExtLib import HTMLIndexCreator
import os
import json
import shutil
import subprocess
import unittest
import TestManager
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
listOfTestSuites = TestManager.TestManager().TestSuites()

def makeTestCasesHtml():
    """
    To display test cases
    """
    chkboxPart1 = "<label><input type=\"checkbox\" name=\""
    chkboxPart2 = "\" value=\""
    chkboxPart3 = "\" class=\"chkTest\">"
    chkboxPart4 = "</label><br><hr>"
    testCases = ""
    for testSuite in listOfTestSuites:
        loadSuite = unittest.TestLoader().loadTestsFromTestCase(testSuite)
        totalTestCases = loadSuite.countTestCases()
        for test in range(totalTestCases):
            strTest = str(loadSuite._tests[test])
            _suiteName = strTest.split('.')[-1][0:-1]
            _testName = strTest.split(' ')[0]
            chkboxValue =  "<"+strTest.split(' ')[1][1:-1]+" testMethod="+_testName+">"
            testCaseName = chkboxPart1+_suiteName+chkboxPart2+chkboxValue+chkboxPart3+_testName+chkboxPart4
            if test == 0:
                suiteLink = "<a id=\"internalReference\" name=\""+_suiteName+"\">"+_suiteName+"</a><hr>"
            else:
                suiteLink = ""
            testCases = testCases + suiteLink + testCaseName
    return testCases

def getAllTestSuiteNames():
    """
    To return the list of test sutie names
    """
    suiteName = []
    for testSuite in listOfTestSuites:
        loadSuite = unittest.TestLoader().loadTestsFromTestCase(testSuite)
        totalTestCases = loadSuite.countTestCases()
        for test in range(totalTestCases):
            strTest = str(loadSuite._tests[test])
            _className = strTest.split('.')[-1][0:-1] # to get the class name alone
            suiteName.append(_className) # appending the class name to suite name
    uniqueSuiteName = list(set(suiteName)) # to get unique testsuites
    return uniqueSuiteName

@route('/selecttests')
def selectTests():
    """
    It will return TestSelector Html page.
    """
    return template('Views/testsuite',serverIpAddress=_serverIpAddress,port=_port,testSuites=getAllTestSuiteNames(),TestCases=makeTestCasesHtml())

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
            shutil.rmtree(pwd+'/Output/')
            os.mkdir(pwd+'/Output/')
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
        subprocess.Popen(['python',pwd+"/ExtLib/Statistics.py","Test Automation",pwd+"/Output/"])
        IndexMaker = HTMLIndexCreator.HTMLIndexCreator(pwd+"/Output/")
        IndexMaker.makeHTMLIndexFile()    
        return "Test completed....."
    else:
        return "The specified runner does not exist."


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

#------------------------------------------------------------------------
@error(404)
def error404(error):
    """
    Handling "404 - Not Found Error"
    """
    return '<strong><center><h3>The Resource you are looking for is currently not available or removed.</h3></center></strong>'

#------------------------------------------------------------------------
@error(500)
def error500(error):
    """
    Handling "500 - Internal Server Error"
    """
    return '<strong><center>The server encountered an unexpected condition which prevented it from fulfilling the request.</center></strong>'

#------------------------------------------------------------------------
@route('/')
def py_runner():
    """
    It will return the home page of the application.
    """
    return template('Views/homepage',serverIpAddress=_serverIpAddress,port=_port)
    
#------------------------------------------------------------------------        
run(host=_serverIpAddress,port=_port,debug=False)
