@echo off
REM === تثبيت المكاتب المطلوبة ===
echo 📦 جاري تثبيت المكاتب...
python -m pip install --upgrade pip
python -m pip install Flask selenium requests

REM === الانتقال إلى مجلد السكربت على سطح المكتب ===
cd /d "%USERPROFILE%\Desktop\SWGE"

REM === تشغيل السكربت ===
echo 🚀 تشغيل SWGE.py...
python SWGE.py

