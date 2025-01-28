#include <Arduino.h>
#include <Servo.h>

#define MAX_POS 80
#define MIN_POS 40

// Create a Servo object to control a servo motor
Servo myServo;

// PIN MAP
// #define PIN_SERVO A0
#define PIN_START PIN0
#define PIN_FUEL PIN1

// Global variables
int degrees = MIN_POS;   // Variable to store new position for the servo
bool led_status = false; // LED status flag
String data = "";        // String to store data from serial input
String command = "";     // String to store command from serial input

// STATES
bool bl_fuel_on = true;
enum state
{
    OFF = 0,
    ON = 1,
    FUEL = 2,
    STARTING = 3,
};
state current_state = OFF;

// Function declarations
void help();
void printBar();
void sweep(int bottom, int top);
int move(int target);
int move_percent(int percent);
void start_engine();

void setup()
{
    // Set the built-in LED pin as an output
    pinMode(LED_BUILTIN, OUTPUT);

    pinMode(PIN_START, OUTPUT);
    pinMode(PIN_FUEL, OUTPUT);

    // Initialize serial communication at 9600 bits per second
    Serial.begin(9600);
    Serial.println("Setting up");

    // Attach the servo on pin A0 to the servo object
    myServo.attach(A0);

    sweep(0, 100);

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
        int delim_pos = command.indexOf(':');
        if (delim_pos < 0)
        {
            delim_pos = command.indexOf(' ');
        }

        if (delim_pos > 0)
        {
            // Extract data and command from the input string
            data = command.substring(delim_pos + 1);
            data.trim();
            degrees = data.toInt();

            command = command.substring(0, delim_pos);
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
            start_engine();
        }
        else if (command == "FUEL")
        {
            bl_fuel_on = !bl_fuel_on;
            Serial.print("Fuel status is: ");
            Serial.println(bl_fuel_on);
        }
        else if (command.startsWith("MOVE") && degrees >= 0)
        {
            // Convert data to an integer and constrain it between 0 and 180
            degrees = move_percent(degrees);
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
        else if (command == "SWEEP")
        {
            sweep(0, 100);
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

void sweep(int bottom, int top)
{

    // Sweep the servo from 0 to 180 degrees
    for (int step = bottom; step <= top; step += 1)
    {
        move_percent(step);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;
        delay(15); // Wait 15 milliseconds for the servo to reach the position
    }

    // Sweep the servo back from 180 to 0 degrees
    for (int step = top; step >= bottom; step -= 1)
    {
        move_percent(step);
        digitalWrite(LED_BUILTIN, led_status);
        led_status = !led_status;
        delay(15); // Wait 15 milliseconds for the servo to reach the position
    }
}

int move(int target)
{
    // degrees = constrain(MAX_POS-target, MIN_POS, MAX_POS);
    degrees = constrain(target, MIN_POS, MAX_POS);
    myServo.write(degrees);
    return degrees;
}

int move_percent(int percent)
{
    return move(100 - map(percent, 0, 100, MIN_POS, MAX_POS));
}

void start_engine()
{

    current_state = STARTING;
    Serial.println("Starting!");

    move_percent(30);
    // enable fuel
    bl_fuel_on = true;
    digitalWrite(PIN_FUEL, true);
    // delay to allow time for fuel to move through the system
    for (int c = 0; c < 5; c++)
    {
        digitalWrite(LED_BUILTIN, true);
        delay(250);
        digitalWrite(LED_BUILTIN, false);
    }

    // Turn on starter motor
    digitalWrite(PIN_START, true);

    // wait two seconds
    digitalWrite(LED_BUILTIN, true);
    delay(2000);
    digitalWrite(LED_BUILTIN, false);

    // turn off starter motor
    digitalWrite(PIN_START, false);
}