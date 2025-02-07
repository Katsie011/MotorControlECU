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
        Serial.println("MOVE: <position> - Move servo to specified position (0-180)");
        Serial.println("FLASH - Flash the LED twice");
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
