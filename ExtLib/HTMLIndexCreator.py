testEngineers = ''

import os
import sys

class HTMLIndexCreator():
    """
    To create an index page for all the HTML test reports.
    This index page will contain all the HTML reports links in the left side and clicking on the link will open the report in the right side.
    Index page template:

    +--------------------------------------------------------+
    |                         Index                          |
    +--------------------------------------------------------+
    | TestSuites |               Results                     |
    +--------------------------------------------------------+
    |Suite1*     |Suite1.html will be loaded in this portion |
    |Suite2      |                                           |
    |Suite3      |                                           |
    |            |                                           |
    |            |                                           |
    +------------+-------------------------------------------+

    ==================================================================================
    Copyright (c) belongs to Parthiban Nithyanantham, All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name Parthiban Nithyanantham nor the names of its contributors may be
      used to endorse or promote products derived from this software without
      specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
    IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ===================================================================================
    """
    def __init__(self,_dir,_theme='skyblue'):
        """
    Getting the HTML Reports directory path and theme(color) from the user.
        """
        self.dir=_dir
        self.theme = _theme
        
    def makeHTMLIndexFile(self):
        """
    This method will create the index.html file in the given directory.
    This method contains the entire source of the index.html file.
        """
        part1 = """<html>
        <body>
        <title>Index</title>
        <div id="container" style="width=100%;text-align:center;">
        <div id="pageTitle" style="background-color:"""+self.theme+""";text-align:left;font-weight:bold;">Index</div>
        <div id="whiteSpace" style="height:0.3%;background-color:white;"></div>
        <div id="TestSuitesTitle" style="width:15%;float:left;background-color:"""+self.theme+""";font-weight:bold;">TestSuites</div>
        <div id="ResultsTitle" style="width:84.7%;float:right;background-color:"""+self.theme+""";font-weight:bold;">Results</div>
        <div id="Suites" style="width:15%;float:left;background-color:lightgrey;font-weight:bold;text-align:left;height:95%;overflow:scroll;">
        """
        part2 = self.makeLinks()
        part3 = """</div>
        <div id="Results" style="width:84.7%;background-color:white;float:right;text-align:left;height:95%;">
        <iframe id="loadHTMLResults" name="loadHTMLResults" frameborder="0" style="height:100%;width:100%;" src="Statistics.html"></iframe>
        </div>
        <div id="footer" style="width:100%;text-align:left;color:lightgrey;background-color:"""+self.theme+""";">Test Engineer(s) :"""+testEngineers+"""</div>
        </div>
        </body>
        </html>
        """
        
        page = (part1+part2+part3)
        f = open(self.dir+'/index.html','w')
        f.write(page)
        f.close
        
    def getHTMLFileNames(self):
        """
        To get .html or .htm files in the mentioned directory
        """
        HTMLFiles = []
        for _file in os.listdir(self.dir):
            if _file.lower().endswith(".html"):
                HTMLFiles.append(_file)
            elif _file.lower().endswith(".htm"):
                HTMLFiles.append(_file)
        return HTMLFiles

    def deleteIndexFileIfExists(self):
	"""
	To delete the index.html file if it is already exists in the mentioned directory.
	"""
	try:
	    os.remove(self.dir+'/index.html')
	except OSError:
	    pass
    
    def makeLinks(self):
        """
        To make TestSuite Links
        """
	self.deleteIndexFileIfExists()
        _fileNames = self.getHTMLFileNames()
        _msgPart1 = "<a href=\""
        _msgPart2 = "\" target=\"loadHTMLResults\">"
        _msgPart3 = "</a><br>"
        _link = ""
        for _fileName in _fileNames:
            _origFileName = _fileName
            _linkName = _fileName.split('.')[0]
            _createAnchorTag = (_msgPart1+str(_origFileName)+_msgPart2+str(_linkName)+_msgPart3)
            _link = _link + _createAnchorTag
        return _link
        
def main(argv):
    if len(argv)<=1:
        print ("Please Enter folder name as first argument and theme(optional) as second argument")
    elif len(argv)==2:
        a = HTMLIndexCreator(str(argv[1]))
        a.makeHTMLIndexFile()
    elif len(argv)==3:
        a = HTMLIndexCreator(str(argv[1]),str(argv[2]))
        a.makeHTMLIndexFile()
    
if __name__ == '__main__':
    main(sys.argv)
