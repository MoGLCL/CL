@echo off
REM === تحديد مسار سطح المكتب ===
set "DESKTOP=%USERPROFILE%\Desktop"

REM === تحديد رابط الملف واسم الملف المؤقت ===
set "URL=https://swultra.ct.ws/cdn/SWGE_250808_120738.zip"
set "ZIP=%DESKTOP%\SWGE.zip"

echo 📥 جاري تحميل الملف...
powershell -command "Invoke-WebRequest '%URL%' -OutFile '%ZIP%'"

echo 📂 جاري فك الضغط على سطح المكتب...
powershell -command "Expand-Archive -Path '%ZIP%' -DestinationPath '%DESKTOP%' -Force"

echo 🗑️ حذف ملف ZIP...
del "%ZIP%"

echo ✅ تم الانتهاء.

