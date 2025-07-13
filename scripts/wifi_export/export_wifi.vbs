' ********** EXPORT_WIFI.VBS **********
CreateObject("Wscript.Shell").Run Chr(34) & _
  WScript.ScriptFullName & Replace(WScript.ScriptName, ".vbs", ".bat") & _
  Chr(34), 0, True

