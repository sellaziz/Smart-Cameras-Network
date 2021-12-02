/**
 * @file MPU9250.ino
 * @author Zijie NING (zijie.ning@imt-atlantique.net)
 * @version 1.0
 * @date 2021-12-02
 *
 */

// I2C protocol
#include "Wire.h"

// I2Cdev and MPU9150 must be installed as libraries
#include "I2Cdev.h"
#include "MPU9150.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU9150 accelGyroMag;

int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;

#define LED_PIN 13
bool blinkState = false;

void setup()
{
    // join I2C bus
    Wire.begin();

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz)
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelGyroMag.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelGyroMag.testConnection() ? "MPU9250 connection successful" : "MPU9250 connection failed");

    // configure Arduino LED pin for output
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    // read raw accel/gyro/mag measurements from device
    // accelGyroMag.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

    // these methods (and a few others) are also available
    // accelGyroMag.getAcceleration(&ax, &ay, &az);
    accelGyroMag.getRotation(&gx, &gy, &gz);

    // display tab-separated accel/gyro/mag x/y/z values
    //  Serial.print("a/g/m:\t");
    //  Serial.print(ax); Serial.print("\t");
    //  Serial.print(ay); Serial.print("\t");
    //  Serial.print(az); Serial.print("\t");
    Serial.print("gx: ");
    Serial.print(gx);
    Serial.print(" ;gy: ");
    Serial.print(gy);
    Serial.print(" gz:");
    Serial.println(gz);

    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
    delay(500);
}
