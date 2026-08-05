' ==========================================
' SCREENSAVER CONFIGURATION OPTIONS
' ==========================================
' You can easily customize the screensaver right here without touching the python code!

' 1. Accent Color
' Change this hex color code to change the theme color of the screensaver. 
' Default is "#8F96BF" (cool blue-grey). Try "#FF5733" for orange, or "#2ECC71" for green.
ACCENT_COLOR = "#8F96BF"

' 2. Windows Key Toggle
' If set to "True", pressing the Windows key will toggle the background light show instead of exiting the screensaver.
' If set to "False", pressing the Windows key will exit the screensaver like normal.
ENABLE_WIN_KEY = "False"

' 3. Screenshot Mode (Strict Exit)
' If set to "True", moving the mouse or pressing random keys WILL NOT exit the screensaver. 
' This is perfect for taking screenshots or locking the screen to purely visual! 
' IMPORTANT: To exit the screensaver when this is True, you MUST press Ctrl + Z.
STRICT_EXIT = "True"

' ==========================================
' SCRIPT LAUNCHER (DO NOT EDIT BELOW)
' ==========================================
Set WshShell = CreateObject("WScript.Shell")
strPath = Wscript.ScriptFullName
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.GetFile(strPath)
strFolder = objFSO.GetParentFolderName(objFile) 
WshShell.CurrentDirectory = strFolder

' Launch python script completely silently in the background and pass our configuration options
strCommand = "pythonw.exe screensaver.py --accent-color """ & ACCENT_COLOR & """ --enable-win-key """ & ENABLE_WIN_KEY & """ --strict-exit """ & STRICT_EXIT & """"
WshShell.Run strCommand, 0, False
