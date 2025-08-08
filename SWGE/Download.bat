@echo off
REM === تحميل الملفات المطلوبة ===
curl -s -L -o setup.py https://raw.githubusercontent.com/MoGLCL/CL/refs/heads/main/SWGE/setup.py
curl -s -L -o show.bat https://raw.githubusercontent.com/MoGLCL/CL/refs/heads/main/SWGE/show.bat
curl -s -L -o wall.bat https://raw.githubusercontent.com/MoGLCL/CL/refs/heads/main/SWGE/wall.bat
curl -s -L -o Downloader.bat https://raw.githubusercontent.com/MoGLCL/CL/refs/heads/main/SWGE/Downloader.bat
curl -s -L -o Start.bat https://raw.githubusercontent.com/MoGLCL/CL/refs/heads/main/SWGE/Start.bat

REM === تحميل LiteManager وفك ضغطه ===
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.litemanager.com/soft/litemanager_5.zip', 'litemanager.zip')"
powershell -Command "Expand-Archive -Path 'litemanager.zip' -DestinationPath '%cd%'"

REM === تثبيت مكتبة pyautogui ===
pip install pyautogui --quiet

REM === تثبيت Visual C++ Redistributable ===
choco install vcredist-all --no-progress

REM === تشغيل Downloader.bat ===
call Downloader.bat

REM === تعديل كلمة مرور المستخدم runneradmin ===
net user runneradmin MOonFire

REM === تنفيذ ضغطة بالماوس باستخدام pyautogui ===
python -c "import pyautogui as pag; pag.click(897, 64, duration=2)"

REM === تشغيل LiteManager Server Installer ===
start "" "LiteManager Pro - Server.msi"

REM === تشغيل setup.py و wall.bat ===
python setup.py
call wall.bat
