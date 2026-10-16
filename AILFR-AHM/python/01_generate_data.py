"""
AILFR-AHM - تولید داده مصنوعی
ساخته شده توسط امیرحسین حاجی مرادخانی
"""

import numpy as np
import random
import os

# مسیر ذخیره داده‌ها
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def generate_line_data(num_samples=10000):
    """
    تولید داده مصنوعی برای ربات خط‌یاب
    
    ۵ سنسور IR:
    - S1: چپ‌ترین
    - S2: چپ
    - S3: وسط
    - S4: راست
    - S5: راست‌ترین
    
    خروجی (۳ کلاس):
    - 0: چپ (Turn Left)
    - 1: مستقیم (Go Straight)
    - 2: راست (Turn Right)
    """
    
    X = []
    y = []
    
    # حالت‌های ممکن
    states = [
        # مستقیم
        ([0, 0, 1, 0, 0], 1),
        ([0, 1, 1, 0, 0], 1),
        ([0, 0, 1, 1, 0], 1),
        # چپ ملایم
        ([0, 1, 1, 0, 0], 0),
        ([1, 1, 1, 0, 0], 0),
        # چپ تند
        ([0, 1, 0, 0, 0], 0),
        ([1, 1, 0, 0, 0], 0),
        ([1, 0, 0, 0, 0], 0),
        # راست ملایم
        ([0, 0, 1, 1, 0], 2),
        ([0, 0, 1, 1, 1], 2),
        # راست تند
        ([0, 0, 0, 1, 0], 2),
        ([0, 0, 0, 1, 1], 2),
        ([0, 0, 0, 0, 1], 2),
        # گم شدن
        ([0, 0, 0, 0, 0], 1),
        ([1, 1, 1, 1, 1], 1),
    ]
    
    for _ in range(num_samples):
        state, action = random.choice(states)
        
        # اضافه کردن نویز کوچیک (برای واقعی‌تر شدن)
        noisy_state = []
        for s in state:
            if random.random() < 0.05:  # ۵٪ نویز
                noisy_state.append(1 - s)
            else:
                noisy_state.append(s)
        
        X.append(noisy_state)
        y.append(action)
    
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int64)
    
    # ذخیره
    np.save(os.path.join(DATA_DIR, "X_train.npy"), X)
    np.save(os.path.join(DATA_DIR, "y_train.npy"), y)
    
    print(f"✅ {num_samples} نمونه تولید شد!")
    print(f"📊 X shape: {X.shape}")
    print(f"📊 y shape: {y.shape}")
    print(f"📊 توزیع کلاس‌ها: {np.bincount(y)}")


if __name__ == "__main__":
    print("=" * 50)
    print("  AILFR-AHM - تولید داده مصنوعی")
    print("=" * 50)
    generate_line_data(10000)