#include <Arduino.h>
#include <Servo.h>

// Create a Servo object to control a servo motor
Servo myServo;

// Global variables
int degrees = 0;          // Variable to store new position for the servo
bool led_status = false; // LED status flag
String data = "";        // String to store data from serial input
String command = "";     // String to store command from serial input

// Function declarations
void help();
void printBar();

void setup()
{
    // Set the built-in LED pin as an output
    pinMode(LED_BUILTIN, OUTPUT);

    // Initialize serial communication at 9600 bits per second
    Serial.begin(9600);
    Serial.println("Setting up");

    // Attach the servo on pin A0 to the servo object
    myServo.attach(A0);

    // Sweep the servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 5)
    {
        myServo.write(pos);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;
        delay(15); // Wait 15 milliseconds for the servo to reach the position
    }

    // Sweep the servo back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 5)
    {
        myServo.write(pos);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;
        delay(15); // Wait 15 milliseconds for the servo to reach the position
    }

    Serial.println("Ready! Let's go!");
    help(); // Display available commands
    Serial.println();
    printBar();
}

void loop()
{
    // Check if data is available to read from the serial port
    if (Serial.available() > 0)
    {
        // Read the incoming string until a newline character
        command = Serial.readStringUntil('\n');
        command.trim(); // Remove any leading or trailing whitespace
        Serial.println("Received:");

        // Find the position of the delimiter ':' or whitespace
        int pos = command.indexOf(':');
        if (pos < 0)
        {
            pos = command.indexOf(' ');
        }

        if (pos > 0)
        {
            // Extract data and command from the input string
            data = command.substring(pos + 1);
            data.trim();
            degrees = data.toInt();

            command = command.substring(0, pos);
            command.trim();
            command.toUpperCase();


            // Echo the command and data for the user
            Serial.print("\t- Command: ");
            Serial.println(command);
            Serial.print("\t- Data: ");
            Serial.println(data);
            Serial.println();
        }
        else
        {
            command.trim();
            command.toUpperCase();

            // Echo the command for the user
            Serial.print("\t- Command: ");
            Serial.println(command);
            Serial.println();
        }

        printBar(); // Print a separator bar

        // Handle different commands
        if (command == "START")
        {
            Serial.println("Running!");
        }
        else if (command.startsWith("MOVE") && degrees >=0)
        {
            // Convert data to an integer and constrain it between 0 and 180
            degrees = constrain(degrees, 0, 180);
            myServo.write(degrees);
            digitalWrite(LED_BUILTIN, led_status);
            led_status = !led_status;
            Serial.print("Moved to: ");
            Serial.println(degrees);

            degrees = -1;
        }
        else if (command == "FLASH")
        {
            // Flash the LED twice
            for (int i = 0; i < 2; i++)
            {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(300);
                digitalWrite(LED_BUILTIN, LOW);
                delay(300);
            }
        }
        else
        {
            help(); // Display available commands if the command is unrecognized
        }

        // Print a separator bar after processing the command
        Serial.println();
        printBar();
        Serial.println();
    }
}

// Function to display available commands
void help()
{
    printBar();
    Serial.println();
    Serial.println("Available commands:");
    Serial.println("START - Begin operation");
    Serial.println("MOVE: <position> - Move servo to specified position (0-180)");
    Serial.println("FLASH - Flash the LED twice");
}

// Function to print a separator bar
void printBar()
{
    for (int i = 0; i < 50; i++)
    {
        Serial.print("#");
    }
    Serial.println();
}