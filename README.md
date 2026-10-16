
# 🤖 AILFR-AHM

**Artificial Intelligence Line Finder Robot** - AHM

هوش مصنوعی خط‌یاب ربات

ساخته شده توسط: **امیرحسین حاجی مرادخانی** 👦

---

## 🎯 چیه؟

مدل هوش مصنوعی برای ربات‌های خط‌یاب که:
- 🧠 با شبکه عصبی (PyTorch) آموزش دیده
- 📥 رایگان برای دانلود
- 🔌 آماده نصب روی آردوینو
- ⚡ سریع و دقیق

---

## 🛠️ سخت‌افزار مورد نیاز

- 🔲 Arduino Uno/Nano/Mega
- 👁️ ۵ سنسور IR
- ⚙️ ۲ موتور DC + درایور L298N
- 🔋 باتری ۹V

---

## 📦 نصب

### مرحله ۱: آموزش مدل
```bash
cd python
pip install -r ../requirements.txt
python 01_generate_data.py
python 02_train_model.py
python 03_export_weights.py
```
##مرحله ۲: آپلود روی آردوینو
Arduino IDE رو باز کن
فایل arduino/AILFR-AHM.ino رو باز کن
برد و پورت رو انتخاب کن

آپلود کن!
---
👨‍💻 سازنده
امیرحسین حاجی مرادخانی 🇮🇷

amirhosseinhajimoradkhani@gmail.com

 https://github.com/amirhossin1395

 ---
 📜 لایسنس
MIT License
---
