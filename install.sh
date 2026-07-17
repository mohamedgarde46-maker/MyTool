#!/bin/bash

# 1. إنشاء مجلد ثابت للأداة داخل النظام
mkdir -p /usr/share/mytool

# 2. نسخ كل ملفات الأداة الحالية إلى هذا المجلد الثابت
cp -r * /usr/share/mytool/

# 3. إنشاء أمر اختصار في النظام باسم mytool ليقوم بتشغيلها من مجلدها الثابت
echo '#!/bin/bash' > /usr/local/bin/mytool
echo 'cd /usr/share/mytool && python3 ku_netscan.py "$@"' >> /usr/local/bin/mytool

# 4. إعطاء صلاحيات التشغيل للأمر الجديد
chmod +x /usr/local/bin/mytool

echo "============================================="
echo "  [+] Done! You can now run the tool using: mytool"
echo "============================================="
#!/bin/bash

# تثبيت المكتبات الخاصة بتعديل الخطوط واللغات الشرقية
pip3 install arabic-reshaper python-bidi --break-system-packages

# إنشاء مجلد ثابت للأداة داخل النظام
mkdir -p /usr/share/mytool
cp -r * /usr/share/mytool/

# إنشاء أمر اختصار في النظام باسم mytool
echo '#!/bin/bash' > /usr/local/bin/mytool
echo 'cd /usr/share/mytool && python3 ku_netscan.py "$@"' >> /usr/local/bin/mytool
chmod +x /usr/local/bin/mytool

echo "Done!"
