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
