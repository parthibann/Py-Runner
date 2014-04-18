import sys
import unittest
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

class functionality1(unittest.TestCase):
    """ Explain about the functionality here
    """
    def setUp(self):
        """ setup required for running testcases.
        """
    
    def tearDown(self):
        """ clear the objects that are created in the setup.
        """
        
    def test_11_testcase1(self):
        """ Explain about testcase1 here.
        I'm simply passing the test case here
        """
        pass
    
    def test_14_testcase2(self):
        """ Explain about testcase2 here.
        I'm simply failing the test case here
        """
        self.fail("failed to demonstrate test failure.")
        
if __name__ == '__main__':
    unittest.main()