@echo off
chcp 65001 >nul
echo 📥 جاري تحميل الملف...
curl -L -o "%USERPROFILE%\Desktop\SWGE.zip" "https://github.com/MoGLCL/CL/releases/download/v3.2/SWGE.zip"

if not exist "%USERPROFILE%\Desktop\SWGE.zip" (
    echo ❌ فشل التحميل.
    pause
    exit /b 1
)

echo 📂 جاري فك الضغط...
powershell -Command "Expand-Archive -Path '%USERPROFILE%\Desktop\SWGE.zip' -DestinationPath '%USERPROFILE%\Desktop\SWGE_TEMP' -Force"

echo 🔄 نقل الملفات إلى سطح المكتب...
powershell -Command "Move-Item -Path '%USERPROFILE%\Desktop\SWGE_TEMP\*' -Destination '%USERPROFILE%\Desktop\' -Force"

echo 🗑️ حذف الملفات المؤقتة...
rmdir /S /Q "%USERPROFILE%\Desktop\SWGE_TEMP"
del "%USERPROFILE%\Desktop\SWGE.zip"

echo ✅ تم الانتهاء.



