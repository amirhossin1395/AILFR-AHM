/*
 * ============================================================
 *   AILFR-AHM
 *   Artificial Intelligence Line Finder Robot
 *   ساخته شده توسط: امیرحسین حاجی مرادخانی
 *   گیت‌هاب: github.com/amirhossin1395
 * ============================================================
 */

#include "model_weights.h"

// ============================================================
//   تعریف پین‌ها
// ============================================================
#define S1 2
#define S2 3
#define S3 4
#define S4 5
#define S5 6

#define ML_F 9
#define ML_B 10
#define MR_F 11
#define MR_B 12

#define SPEED 150

// ============================================================
//   Setup
// ============================================================
void setup() {
  Serial.begin(9600);
  
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(S3, INPUT);
  pinMode(S4, INPUT);
  pinMode(S5, INPUT);
  
  pinMode(ML_F, OUTPUT);
  pinMode(ML_B, OUTPUT);
  pinMode(MR_F, OUTPUT);
  pinMode(MR_B, OUTPUT);
  
  Serial.println(F("AILFR-AHM Ready!"));
}

// ============================================================
//   پیش‌بینی با شبکه عصبی
// ============================================================
int predict(float input[5]) {
  // ===== لایه اول: 5 -> 8 =====
  float h1[8];
  for (int i = 0; i < 8; i++) {
    float sum = pgm_read_float(&b1[i]);
    for (int j = 0; j < 5; j++) {
      sum += input[j] * pgm_read_float(&W1[j * 8 + i]);
    }
    h1[i] = (sum > 0) ? sum : 0;
  }
  
  // ===== لایه دوم: 8 -> 8 =====
  float h2[8];
  for (int i = 0; i < 8; i++) {
    float sum = pgm_read_float(&b2[i]);
    for (int j = 0; j < 8; j++) {
      sum += h1[j] * pgm_read_float(&W2[j * 8 + i]);
    }
    h2[i] = (sum > 0) ? sum : 0;
  }
  
  // ===== لایه خروجی: 8 -> 3 =====
  float out[3];
  for (int i = 0; i < 3; i++) {
    float sum = pgm_read_float(&b3[i]);
    for (int j = 0; j < 8; j++) {
      sum += h2[j] * pgm_read_float(&W3[j * 3 + i]);
    }
    out[i] = sum;
  }
  
  // ===== بیشترین مقدار =====
  int maxIdx = 0;
  for (int i = 1; i < 3; i++) {
    if (out[i] > out[maxIdx]) maxIdx = i;
  }
  return maxIdx;
}

// ============================================================
//   کنترل موتور
// ============================================================
void goForward() {
  analogWrite(ML_F, SPEED); analogWrite(ML_B, 0);
  analogWrite(MR_F, SPEED); analogWrite(MR_B, 0);
}

void turnLeft() {
  analogWrite(ML_F, 0); analogWrite(ML_B, SPEED);
  analogWrite(MR_F, SPEED); analogWrite(MR_B, 0);
}

void turnRight() {
  analogWrite(ML_F, SPEED); analogWrite(ML_B, 0);
  analogWrite(MR_F, 0); analogWrite(MR_B, SPEED);
}

void stopMotors() {
  analogWrite(ML_F, 0); analogWrite(ML_B, 0);
  analogWrite(MR_F, 0); analogWrite(MR_B, 0);
}

// ============================================================
//   حلقه اصلی
// ============================================================
void loop() {
  float sensors[5];
  sensors[0] = !digitalRead(S1);
  sensors[1] = !digitalRead(S2);
  sensors[2] = !digitalRead(S3);
  sensors[3] = !digitalRead(S4);
  sensors[4] = !digitalRead(S5);
  
  int action = predict(sensors);
  
  if (action == 0) turnLeft();
  else if (action == 1) goForward();
  else if (action == 2) turnRight();
  
  delay(10);
}