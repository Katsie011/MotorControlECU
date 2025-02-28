#ifndef SETTINGS_H
#define SETTINGS_H
#include <Arduino.h>
#include <Servo.h>

#define BAUD_RATE 9600

// PIN MAP
#define PIN_SERVO PIN_A0
#define PIN_START PIN3
#define PIN_FUEL PIN2   
#define PIN_AUX_INDICATOR PIN4


// ENGINE SETTINGS:
#define MAX_POS 90
#define MIN_POS 0
#define IDLE_PERCENT 73

#define START_TIME_MS 1500 
#define FUEL_PRIME_TIME_MS 1000 

#endif //SETTINGS_H
