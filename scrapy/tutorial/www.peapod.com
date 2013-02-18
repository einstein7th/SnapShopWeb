<HTML>

<HEAD>
<TITLE>Peapod Expired Session</TITLE>
</HEAD>

<script language="JavaScript">
   <!-- Begin to hide script contents from old browsers.
   var bNow = new Date();
   var bNum = bNow.getTime();

   function redirect()
   {
     var uPath = document.location.pathname;
     var uDir = uPath.substr(0, ((uPath.lastIndexOf('/') + 1)));
     var newLocation = document.location.protocol  + "//" + document.location.host + uDir + "expiredSession.html?NUM1=" + bNum;
     top.location.replace(newLocation);
   }
// End the hiding here. -->
</script>

<BODY ONLOAD="javascript:redirect();">

<div id="x-action-id" style="display:none" x-action="redirect" x-action-url="expiredSession.html"></div>

</BODY>
</HTML>

