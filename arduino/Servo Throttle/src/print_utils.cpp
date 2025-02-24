#include <Arduino.h>
#include "print_utils.h"

namespace printUtils
{
    // Function to display available commands
    void print_help()
    {
        print_bar();
        Serial.println();
        Serial.println("Available commands:");
        Serial.println("START - Begin operation");
        Serial.println("FUEL - Toggle Fuel State (ON/OFF)");
        Serial.println("MOVE: <position> - Move servo to specified position (min pos - max pos)");
        Serial.println("SWEEP - Sweep the throttle from min to max position");
        Serial.println("FLASH - Flash the Arduino Builtin LED twice to test");
        Serial.println("STATE - Report current open loop engine state");
        Serial.println("UMOVE: <position> - UNSAFE Move servo to specified position (0-180)");
    }

    // Function to print a separator bar
    void print_bar()
    {
        for (int i = 0; i < 50; i++)
        {
            Serial.print("#");
        }
        Serial.println();
    }
}
