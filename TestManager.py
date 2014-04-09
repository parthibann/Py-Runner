from Test.Modules.Module1 import functionality1_tests
from Test.Modules.Module1 import functionality2_tests
from Test.Modules.Module2 import functionality3_tests
from Test.Modules.Module2 import functionality4_tests

class TestManager():
    """ To manage all the TestSuites
    """
    def TestSuites(self):
        """All the TestSuites are called here and returned as a list. 
        """
        module1 = []
        module1.append(functionality1_tests.functionality1)
        module1.append(functionality2_tests.functionality2)
        
        module2 = []
        module2.append(functionality3_tests.functionality3)
        module2.append(functionality4_tests.functionality4)
        
        testSuites = module1 + module2
        return testSuites