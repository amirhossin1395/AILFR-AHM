"""
AILFR-AHM - آموزش مدل با PyTorch (نسخه با Seed ثابت)
ساخته شده توسط امیرحسین حاجی مرادخانی
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import random

# ========================================
# 🎯 Seed ثابت (برای تکرارپذیری)
# ========================================
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

# ========================================
# مسیرها
# ========================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

# ========================================
# بارگذاری داده‌ها
# ========================================
print("📥 بارگذاری داده‌ها...")
X = np.load(os.path.join(DATA_DIR, "X_train.npy"))
y = np.load(os.path.join(DATA_DIR, "y_train.npy"))

# تقسیم به آموزش و تست (با Seed ثابت)
indices = np.random.permutation(len(X))
split = int(0.8 * len(X))
train_idx, test_idx = indices[:split], indices[split:]

X_train = torch.tensor(X[train_idx])
y_train = torch.tensor(y[train_idx])
X_test = torch.tensor(X[test_idx])
y_test = torch.tensor(y[test_idx])

print(f"📊 داده آموزش: {len(X_train)}")
print(f"📊 داده تست: {len(X_test)}")

# ========================================
# ساخت مدل
# ========================================
print("\n🧠 ساخت مدل...")


class AILFR_Model(nn.Module):
    def __init__(self):
        super(AILFR_Model, self).__init__()
        self.fc1 = nn.Linear(5, 8)   # ورودی ۵ → مخفی ۸
        self.fc2 = nn.Linear(8, 8)   # مخفی ۸ → مخفی ۸
        self.fc3 = nn.Linear(8, 3)   # مخفی ۸ → خروجی ۳
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


model = AILFR_Model()
print(model)

# ========================================
# کامپایل و آموزش
# ========================================
print("\n🎓 شروع آموزش...")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

epochs = 100
batch_size = 32

for epoch in range(epochs):
    model.train()
    
    # Shuffle (با Seed)
    perm = torch.randperm(len(X_train))
    X_train_shuffled = X_train[perm]
    y_train_shuffled = y_train[perm]
    
    total_loss = 0
    
    for i in range(0, len(X_train), batch_size):
        batch_X = X_train_shuffled[i:i + batch_size]
        batch_y = y_train_shuffled[i:i + batch_size]
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        model.eval()
        with torch.no_grad():
            outputs = model(X_test)
            _, predicted = torch.max(outputs, 1)
            accuracy = (predicted == y_test).float().mean().item()
        
        print(f"Epoch {epoch + 1}/{epochs} | Loss: {total_loss:.4f} | Accuracy: {accuracy * 100:.2f}%")

# ========================================
# ارزیابی نهایی
# ========================================
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, predicted = torch.max(outputs, 1)
    final_accuracy = (predicted == y_test).float().mean().item()

print(f"\n🎯 دقت نهایی: {final_accuracy * 100:.2f}%")

# ========================================
# ذخیره مدل
# ========================================
model_path = os.path.join(MODEL_DIR, "AILFR-AHM.pt")
torch.save(model.state_dict(), model_path)
print(f"\n✅ مدل ذخیره شد: {model_path}")

# ========================================
# ذخیره دقت
# ========================================
with open(os.path.join(MODEL_DIR, "accuracy.txt"), "w") as f:
    f.write(str(final_accuracy * 100))