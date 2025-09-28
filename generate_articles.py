import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

# مجلد المقالات
ARTICLES_DIR = "articles"
OUTPUT_FILE = "articles.json"

articles_list = []

for filename in os.listdir(ARTICLES_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(ARTICLES_DIR, filename)
        
        # قراءة محتوى الملف
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # استخراج العنوان من <title>
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string if soup.title else filename
        
        # تاريخ آخر تعديل
        mod_time = os.path.getmtime(filepath)
        date_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
        
        # إضافة للمصفوفة
        articles_list.append({
            "title": title.strip(),
            "file": os.path.join(ARTICLES_DIR, filename),
            "date": date_str
        })

# ترتيب المقالات من الأحدث إلى الأقدم
articles_list.sort(key=lambda x: x["date"], reverse=True)

# حفظ في JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(articles_list, out, ensure_ascii=False, indent=2)

print(f"تم تحديث {OUTPUT_FILE} بعدد مقالات: {len(articles_list)}")
