#ifndef ENGINE_UTILS_H
#define ENGINE_UTILS_H

namespace Engine
{
    // STATES
    enum state
    {
        OFF = 0,
        ON = 1,
        FUEL = 2,
        STARTING = 3,
    };

    // Function declarations
    void setup(int pin);
    void flash_pin(int pin, int times, int duration);
    void sweep_percent(int bottom, int top);
    int move(int target);
    int move_percent(int percent);
    int unconstrained_move(int target);
    void start_engine();
    void stop_engine();


    state get_engine_state();
    bool toggle_fuel();
}

#endif // ENGINE_UTILS_H