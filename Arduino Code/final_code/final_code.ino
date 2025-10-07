#include <Servo.h>

Servo servo1, servo2, servo3, servo4;

void setup() {
  Serial.begin(9600);

  servo1.attach(5);
  servo2.attach(6);
  servo3.attach(9);
  servo4.attach(10);

  // Set initial positions
  servo1.write(90);
  servo2.write(120);
  servo3.write(120);
  servo4.write(180);
}

void loop() {
  if (Serial.available()) {
    char input = Serial.read();
    Serial.print("Received: ");
    Serial.println(input);

    // Reset all servos before starting
    servo1.write(90);
    servo2.write(120);
    servo3.write(120);
    servo4.write(180);
    delay(5000);

    if (input == '1') {
      runSequence1();
    } else if (input == '2') {
      runSequence2();
    }
  }
}

void moveSmooth(Servo& servo, int fromAngle, int toAngle) {
  int step = (toAngle > fromAngle) ? 1 : -1;
  for (int pos = fromAngle; pos != toAngle; pos += step) {
    servo.write(pos);
    delay(15);
  }
  servo.write(toAngle);
}

void runSequence1() {
  moveSmooth(servo3, 120, 80);
  delay(5000);

  moveSmooth(servo3, 80, 60); 
  delay(5000);

  moveSmooth(servo3, 60, 50);
  delay(5000);

  moveSmooth(servo2, 120, 130);
  delay(1000);

  moveSmooth(servo4, 180, 160);
  delay(2000);

  moveSmooth(servo4, 160, 120); 
  delay(5000);
  
  moveSmooth(servo4, 120, 115);
  delay(5000);
  
  moveSmooth(servo2, 125, 90);
  delay(1000);
  moveSmooth(servo3, 50, 80);
  delay(5000);

  moveSmooth(servo1, 90, 10);
  delay(2000);

  moveSmooth(servo4, 115, 180);
  delay(5000);
}

void runSequence2() {
moveSmooth(servo3, 120, 80);
  delay(5000);

  moveSmooth(servo2, 120, 130);
  delay(5000);

  moveSmooth(servo3, 80, 60);
  delay(5000);

  moveSmooth(servo3, 60, 50);
  delay(1000);

  moveSmooth(servo2, 130, 125);
  delay(2000);

  moveSmooth(servo4, 180, 150);
  delay(5000);
  
  moveSmooth(servo4, 150, 130);
  delay(5000);
  
  moveSmooth(servo4, 130, 125);
  delay(5000);

  moveSmooth(servo2, 125, 90);
  moveSmooth(servo3, 50, 80);
  delay(1000);

  moveSmooth(servo1, 90, 170);
  delay(2000);

  moveSmooth(servo4, 125, 180);
  delay(5000);
}
