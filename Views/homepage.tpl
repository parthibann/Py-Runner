<html>
<body>
<title>Test Automation</title>
<div id="container">
<div id="pageTitle">Computenext API Test Automation</div>
<div id="space" style="height:0.3%;"></div>
<div id="resourceLinksContainer">
<table>
<tr>
<td><a href="http://{{serverIpAddress}}:{{port}}/selecttests" target="frame">TestSuites</a></td>
<td>| <a href="http://{{serverIpAddress}}:{{port}}/results/" target="frame">Results</a></td>
</tr>
</table>
</div>
<iframe id="frame" name="frame" src="http://{{serverIpAddress}}:{{port}}/selecttests"></iframe>
</div>
</body>
</html>
<style>
body{
margin:1;
}
a{
color:white;
}
#container{
text-align:center;
}
#pageTitle{
background-color:#3b5998;
color:white;
font-size:18pt;
font-weight:bold;
}
#resourceLinksContainer{
background-color:#3b5998;
font-size:10pt;
font-weight:bold;
}
#frame{
height:91.5%;
width:99.8%;
background-color:#edf0f5;
}
</style>