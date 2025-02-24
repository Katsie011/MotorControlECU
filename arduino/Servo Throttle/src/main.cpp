#include "settings.h"
#include "engine_utils.h"
#include "print_utils.h"

// Global variables
int degrees = MIN_POS;   // Variable to store new position for the servo
bool led_status = false; // LED status flag
String data = "";        // String to store data from serial input
String command = "";     // String to store command from serial input

void setup()
{
    // Set the built-in LED pin as an output
    pinMode(LED_BUILTIN, OUTPUT);
    // hardware outputs on the engine
    pinMode(PIN_START, OUTPUT);
    pinMode(PIN_FUEL, OUTPUT);
    pinMode(PIN_AUX_INDICATOR, OUTPUT);

    // Initialize serial communication at 9600 bits per second
    Serial.begin(BAUD_RATE);
    Serial.println("Setting up");

    // Attach the servo and sweep
    Engine::setup(PIN_SERVO);

    Serial.println("Ready! Let's go!");
    printUtils::print_help(); // Display available commands
    Serial.println();
    printUtils::print_bar();
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

        printUtils::print_bar(); // Print a separator bar

        // Handle different commands
        if (command == "START")
        {
            Engine::start_engine();
        }
        else if (command == "STOP")
        {
            Engine::stop_engine();
        }
        else if (command == "FUEL")
        {
            Serial.print("Fuel status is now: ");
            Serial.println(Engine::toggle_fuel());
        }
        else if ((command.startsWith("MOVE") ||
                  command.equals("M")) &&
                 degrees >= 0)
        {
            // Convert data to an integer and constrain it between 0 and 180
            degrees = Engine::move_percent(degrees);
            digitalWrite(LED_BUILTIN, led_status);
            led_status = !led_status;
            Serial.print("Moved to: ");
            Serial.println(degrees);
            degrees = -1;
        }
        else if (command.startsWith("UMOVE") && degrees >= 0)
        {
            // Unsafe move!
            degrees = Engine::unconstrained_move(degrees);
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
            Engine::sweep_percent(0, 100);
        }
        else if (command == "STATE")
        {
            // TODO this returns a number for now. Need to convert the number to text.

            Serial.print("Current engine status is: ");
            Serial.println(Engine::get_engine_state());
        }
        else
        {
            printUtils::print_help(); // Display available commands if the command is unrecognized
        }

        // Print a separator bar after processing the command
        Serial.println();
        printUtils::print_bar();
        Serial.println();
    }
}
