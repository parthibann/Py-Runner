Py-Runner
=========

  * Py-Runner is a template for python's unittest framework.
  * The features that Py-Runner provide are :
      * Web-UI for selecting test cases.
      * Generate HTML reports.
      * Integrated with Testlink (test case management application, so that results are stored in DataBase and you can use the reports that are generated from testlink as well)


## External Libraries : ##

  * [Bottle](https://github.com/defnull/bottle "Bottle") - Bottle is used as web framework and web server in this project (single threaded web server) for more information about bottle please refer bottle documentation.
  * [HTML Test Runner](https://github.com/tungwaiyip/HTMLTestRunner "HTML Test Runner") - HTMLTestRunner is an extension to the Python standard library's unittest module, It generates easy to use HTML test reports, HTMLTestRunner is released under a BSD style license, Only a single file module HTMLTestRunner.py is needed to generate your report, For more information about HTMLTestRunner please refer HTMLTestRunner documentation.
  * [HTML Index Creator](https://github.com/parthibann/HTMLIndexCreator "HTML Index Creator") - Used to create an index file for all the HTML Test Reports.
  * [Testlink Runner](https://github.com/parthibann/Python-TestLink-Runner "Testlink Runner") - Testlink runner is used to post the automation results to testlink api, so that results are stored in testlink database.

Thanks to all the contributors of the above mentioned projects.

## Usage : ##

  * Clone this project `git clone https://github.com/parthibann/Py-Runner.git`
  * Edit app.py file and update your server ip address in "_serverIpAddress" variable and testlink xmlrpc link in "_testlinkURL" variable.
  * Run the application `python app.py`
  * open borwser and log on to the url `http://ipaddress:port`, it will open the py-unittestRunner home page. 
  * Click on the TestSelector link to view your testsuites and testcases.
  * select test cases and click run button to run the testcases, once the test cases are completed you get a pop-up stating "test(s) completed..."
  * once you got that pop-up click the results link for viewing the results.

## System Requirements : ##

  * Python 2.7 or above

## Explanation : ##

  * This project follows the following tree structure (not necessary to follow the same structure) :
![py-runner](https://cloud.githubusercontent.com/assets/4667360/2958070/0f029822-daa6-11e3-9bb2-e3892e0e587f.PNG)
