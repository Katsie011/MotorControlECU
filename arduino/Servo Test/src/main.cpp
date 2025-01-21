#include <Arduino.h>
#include <Servo.h>

Servo myServo;

int newPos = 0;
bool led_status = false;
void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    // Initialize serial communication at 9600 bits per second:
    Serial.begin(9600);
    Serial.println("Setting up");

    // Attach the servo on pin 9 to the servo object
    myServo.attach(A0);

    // Sweep the servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos++)
    {
        myServo.write(pos);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;

        delay(15); // Wait 50 milliseconds for the servo to reach the position
        
    }

    // Sweep the servo back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos--)
    {
        myServo.write(pos);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;
        delay(15); // Wait 50 milliseconds for the servo to reach the position
    }
}

void loop()
{
    // Check if data is available to read
    if (Serial.available() > 0)
    {
        // Read the incoming byte:
        newPos = Serial.parseInt();

        // Constrain the position to be within 0 to 180 degrees
        newPos = constrain(newPos, 0, 180);

        // Move the servo to the new position
        myServo.write(newPos);

        Serial.print("Moved to: ");
        Serial.println(newPos);
    }

    digitalWrite(LED_BUILTIN, led_status);
    led_status = !led_status;
    delay(300);
}
