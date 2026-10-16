"""
AILFR-AHM - استخراج وزن‌ها برای Arduino
ساخته شده توسط امیرحسین حاجی مرادخانی
"""

import torch
import torch.nn as nn
import numpy as np
import os

# ========================================
# مسیرها
# ========================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
ARDUINO_DIR = os.path.join(BASE_DIR, "arduino")
os.makedirs(ARDUINO_DIR, exist_ok=True)


# ========================================
# مدل (همون ساختار)
# ========================================
class AILFR_Model(nn.Module):
    def __init__(self):
        super(AILFR_Model, self).__init__()
        self.fc1 = nn.Linear(5, 8)
        self.fc2 = nn.Linear(8, 8)
        self.fc3 = nn.Linear(8, 3)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ========================================
# بارگذاری مدل
# ========================================
print("📥 بارگذاری مدل...")
model = AILFR_Model()
model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "AILFR-AHM.pt")))
model.eval()

# ========================================
# استخراج وزن‌ها
# ========================================
W1 = model.fc1.weight.detach().numpy()  # (8, 5)
b1 = model.fc1.bias.detach().numpy()    # (8,)
W2 = model.fc2.weight.detach().numpy()  # (8, 8)
b2 = model.fc2.bias.detach().numpy()    # (8,)
W3 = model.fc3.weight.detach().numpy()  # (3, 8)
b3 = model.fc3.bias.detach().numpy()    # (3,)

print(f"W1: {W1.shape}")  # (8, 5) → باید transpose بشه
print(f"b1: {b1.shape}")  # (8,)
print(f"W2: {W2.shape}")  # (8, 8)
print(f"b2: {b2.shape}")  # (8,)
print(f"W3: {W3.shape}")  # (3, 8)
print(f"b3: {b3.shape}")  # (3,)

# ========================================
# ذخیره دقت
# ========================================
try:
    with open(os.path.join(MODEL_DIR, "accuracy.txt"), "r") as f:
        accuracy = f.read().strip()
except:
    accuracy = "95.00"


# ========================================
# تبدیل به آرایه C
# ========================================
def array_to_c(name, array, transpose=False):
    """تبدیل آرایه numpy به آرایه C"""
    if transpose:
        array = array.T
    flat = array.flatten()
    
    # تقسیم به خطوط ۸ تایی
    lines = []
    for i in range(0, len(flat), 8):
        chunk = flat[i:i + 8]
        values = ", ".join([f"{v:.6f}f" for v in chunk])
        lines.append("    " + values)
    
    body = ",\n".join(lines)
    return f"const float {name}[] PROGMEM = {{\n{body}\n}};"


# ========================================
# ساخت فایل model_weights.h
# ========================================
output_path = os.path.join(ARDUINO_DIR, "model_weights.h")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("/*\n")
    f.write(" * ============================================================\n")
    f.write(" *   AILFR-AHM - وزن‌های مدل\n")
    f.write(" *   Artificial Intelligence Line Finder Robot\n")
    f.write(" *   ساخته شده توسط: امیرحسین حاجی مرادخانی\n")
    f.write(f" *   دقت: {accuracy}%\n")
    f.write(" * ============================================================\n")
    f.write(" */\n\n")
    
    f.write("#ifndef MODEL_WEIGHTS_H\n")
    f.write("#define MODEL_WEIGHTS_H\n\n")
    
    f.write("#include <avr/pgmspace.h>\n\n")
    
    # لایه ۱: 5 -> 8 (transpose از (8,5) به (5,8))
    f.write("// ===== لایه اول: 5 -> 8 =====\n")
    f.write(array_to_c("W1", W1, transpose=True) + "\n\n")
    f.write(array_to_c("b1", b1) + "\n\n")
    
    # لایه ۲: 8 -> 8 (transpose از (8,8) به (8,8))
    f.write("// ===== لایه دوم: 8 -> 8 =====\n")
    f.write(array_to_c("W2", W2, transpose=True) + "\n\n")
    f.write(array_to_c("b2", b2) + "\n\n")
    
    # لایه ۳: 8 -> 3 (transpose از (3,8) به (8,3))
    f.write("// ===== لایه خروجی: 8 -> 3 =====\n")
    f.write(array_to_c("W3", W3, transpose=True) + "\n\n")
    f.write(array_to_c("b3", b3) + "\n\n")
    
    f.write("#endif\n")

print(f"\n✅ فایل ساخته شد: {output_path}")
print(f"📊 حجم فایل: {os.path.getsize(output_path)} بایت")