#include "settings.h"
#include "engine_utils.h"

namespace Engine
{

    bool bl_fuel_on = true;
    state current_state = OFF;
    // Create a Servo object to control a servo motor
    Servo throttleServo;

    void setup(int pin)
    {
        throttleServo.attach(PIN_SERVO);
        Engine::sweep_percent(0, 100);
    }

    state get_engine_state()
    {
        return current_state;
    }
    void sweep_percent(int bottom, int top)
    {
        bool led_status = false;
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

    void flash_pin(int pin, int times, int duration)
    {
        // TODO change this to not use a delay
        for (int i = 0; i <= times; i++)
        {
            digitalWrite(LED_BUILTIN, true);
            digitalWrite(pin, true);
            delay(duration/2);

            digitalWrite(LED_BUILTIN, false);
            digitalWrite(pin, false);
            // delay if not the last flash
            if (i != times)
            {
                delay(duration/2);
            }
        }
    }

    int move(int target)
    {
        // degrees = constrain(MAX_POS-target, MIN_POS, MAX_POS);
        int degrees = constrain(target, MIN_POS, MAX_POS);
        throttleServo.write(degrees);
        return degrees;
    }
    int unconstrained_move(int target)
    {
        // degrees = constrain(MAX_POS-target, MIN_POS, MAX_POS);
        throttleServo.write(target);
        return target;
    }
    int move_percent(int percent)
    {
        return move(100 - map(percent, 0, 100, MIN_POS, MAX_POS));
    }

    bool toggle_fuel()
    {
        bl_fuel_on = !bl_fuel_on;
        digitalWrite(PIN_FUEL, bl_fuel_on);
        return bl_fuel_on;
    }

    void start_engine()
    {

        current_state = STARTING;
        Serial.println("Starting!");

        Engine::move_percent((IDLE_PERCENT+MAX_POS)/2);
        // enable fuel
        bl_fuel_on = true;
        digitalWrite(PIN_FUEL, true);
        digitalWrite(PIN_AUX_INDICATOR, true);

        // delay to allow time for fuel to move through the system
        Serial.println("\tPriming fuel");
        flash_pin(PIN_AUX_INDICATOR, 15, 100);

        // wait 1.5 seconds
        digitalWrite(PIN_START, true); // starter on
        Serial.println("\tStarter ON");
        flash_pin(PIN_AUX_INDICATOR, 3, 500);
        // turn off starter motor
        digitalWrite(PIN_START, false); //starter off
        Serial.println("\tStarter OFF");

        // Start indicator off.
        
        Serial.println("\tBack to idle");
        Engine::move_percent(IDLE_PERCENT);
        Serial.println("\tWait a little for the engine to settle");
        flash_pin(PIN_AUX_INDICATOR, 4, 250);
        Serial.println("\tDone!");
    }

    void stop_engine()
    {
        Serial.println("Stopping!");
        Serial.println("\tThrottling down");
        Engine::move_percent(MIN_POS);
        Serial.println("\tFuel off");
        digitalWrite(PIN_FUEL, false);
        current_state = OFF;

        Serial.println("\tWaiting...");
        flash_pin(PIN_AUX_INDICATOR, 15, 100);
        Serial.println("\tDone!");
    }
}