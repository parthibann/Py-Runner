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
$.ajax({type:'POST',url:"http://{{serverIpAddress}}:{{port}}/runtest",data : JSON.stringify({"testCases":testCases,"Runner":selectedRunner,"userId":userId,"testPlanId":testPlanId,"buildName":buildName}),dataType: "json",success:function(){alert('success')},error: function(e){alert(JSON.stringify(e))},contentType: "application/json; charset=utf-8"});
});
$('.selectAllTestCases').click( function(){
$('.chkTest').prop('checked',$(this).is(':checked'));
});
% for suite in testSuites:
$('.{{suite}}').click( function(){$('input[name={{suite}}]').prop('checked',$(this).is(':checked'));});
% end
});
</script>
</head>
<body><title>TestSuites & TestCases</title>
<div id="container">
<div id="testSuitesTitle">TestSuites</div>
<div id="testcasesTitle">TestCases</div>
<div id="testSuites">
% for suite in testSuites:
<input type="checkbox" name="{{suite}}" class="{{suite}}"><a href="#{{suite}}">{{suite}}</a><br>
% end
</div>
<div id="testCases">
{{!TestCases}}
</div>
<div id="TLRunner" style="background-color:lightgrey;font-weight:bold;text-align:center;width:100%;display:none;">User Id:
<input type="text" name="useridtxtbox" placeholder="Enter User Id *" size=14>TestPlan Id :
<input type="text" name="testplantxtbox" placeholder="Enter TestPlan Id *" size=14>Build Name :
<input type="text" name="buildnametxtbox" placeholder="Enter Build Name *" size=14></div>
<div id="runner">Select Runner : 
<input type="radio" name="testRunner" class="runnerRadio" value="HTMLTestRunner" checked>HTMLTestRunner
<input type="radio" name="testRunner" class="runnerRadio" value="TestLinkRunner">TestLinkRunner
<input type="checkbox" class="selectAllTestCases" />Select All Test Cases
<button type="button" class="RunSelectedTests">Run</button></div>
</div>
</body>
</html>
<style>
body{
margin:0;
}
#container{
width:100%;
text-align:center;
}
#testSuitesTitle{
font-weight:bold;
float:left;
width:25%;
background-color:#6495ED;
color:white;
}
#testcasesTitle{
background-color:#6495ED;
font-weight:bold;
float:right;
width:75%;
color:white;
}
#testSuites{
background-color:lightgrey;
font-weight:bold;
float:left;
width:25%;
text-align:left;
height:93%;
overflow:scroll;
}
#testCases{
background-color:white;
font-weight:bold;
float:right;
width:75%;
height:93%;
text-align:left;
overflow:scroll;
}
#runner{
background-color:#6495ED;
font-weight:bold;
text-align:center;
width:100%;
}
#internalReference{
background-color:yellow;
}
</style>
