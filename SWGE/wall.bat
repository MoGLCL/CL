@echo off
set "URL=https://swultra.ct.ws/wall/wall.jpg"
set "TEMPIMG=%TEMP%\wallpaper.jpg"

REM تحميل الصورة للرابط
powershell -Command "Invoke-WebRequest '%URL%' -OutFile '%TEMPIMG%'"

REM تغيير الخلفية
powershell -Command "Add-Type 'using System.Runtime.InteropServices; public class Wallpaper { [DllImport(\"user32.dll\", SetLastError=true)] public static extern bool SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni); }'; [Wallpaper]::SystemParametersInfo(20, 0, '%TEMPIMG%', 3)"



