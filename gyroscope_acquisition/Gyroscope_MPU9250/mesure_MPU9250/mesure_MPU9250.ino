/**
   @file mesure_MPU9250.ino
   @author Zijie NING (zijie.ning@imt-atlantique.net)
   @version 3.1
   @date 2021-12-02

   Arduino library "MPU9250" by hideakitai (https://github.com/hideakitai/MPU9250)

   Control gyroscope MPU9250 with calibration.
   Type '1' to save data via serial port.

*/

#include "MPU9250.h"

MPU9250 mpu;
int count = 0;
char command;

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  delay(200);

  if (!mpu.setup(0x68))
  { // change to your own address
    while (1)
    {
      Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
      delay(1000);
    }
  }

  // calibrate anytime you want to
  Serial.println("Accel Gyro calibration will start in 5sec.");
  Serial.println("Please leave the device still on the flat plane.");
  mpu.verbose(true);
  delay(5000);
  mpu.calibrateAccelGyro();

  Serial.println("Mag calibration will start in 5sec.");
  Serial.println("Please Wave device in a figure eight until done.");
  delay(5000);
  mpu.calibrateMag();

  print_calibration();
  mpu.verbose(false);

  Serial.println("Ready to go !");
  Serial.print("Test Yaw Pitch Roll");
}

void loop()
{
  mpu.update();

  static uint32_t prev_ms = millis();
  if (millis() > prev_ms + 100)
  {
    Serial.println("");
    Serial.print(count);
    print_roll_pitch_yaw();
    prev_ms = millis();
  }

  if (Serial.available() > 0)
  {
    command = Serial.read();
    if (command == '1')
    {
      count++;
      Serial.print(" save");
    }
  }
  while (Serial.read() >= 0)
  {
  }
}

void print_roll_pitch_yaw()
{
  // Serial.print(" Yaw,Pitch,Roll: ");
  Serial.print(" ");
  Serial.print(mpu.getYaw(), 2);
  Serial.print(" ");
  Serial.print(mpu.getPitch(), 2);
  Serial.print(" ");
  Serial.print(mpu.getRoll(), 2);
}

void print_calibration()
{
  Serial.println("< calibration parameters >");
  Serial.println("accel bias [g]: ");
  Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.println();
  Serial.println("gyro bias [deg/s]: ");
  Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.println();
  Serial.println("mag bias [mG]: ");
  Serial.print(mpu.getMagBiasX());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasZ());
  Serial.println();
  Serial.println("mag scale []: ");
  Serial.print(mpu.getMagScaleX());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleY());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleZ());
  Serial.println();
}
