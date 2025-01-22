---
title: Overarching plan for the system
---
# Overarching plan for the system


## Communications:

CANController (rpi) -- serial --> arduino
arduino -- serial --> servo
servo -- mechanical --> engine throttle

### Inputs
speedSensor -- CAN --> rpi
VCUSpeedCommand -- CAN --> rpi
servoPosition -- serial --> rpi (possible if we have the right servo)

### In the controller:
abs(SpeedCommand - current speed) = error
SpeedCommand +  error --> PID
PID --> throttle command

``` mermaid
graph TD;
    VCU[VCU] --> speedCommand -->|CAN| rpi[Raspberry Pi];
    speedSensor[Speed Sensor] -->|CAN| rpi;
    rpi -->|serial| arduino[Arduino];
    arduino -->|PWM| servo[Servo];
    servo -->|mechanical| throttle[Engine Throttle];
    rpi -->|GPIO| contactor[Contactor];
    contactor -->|engages| starterMotor[Starter Motor];
    starterMotor --> engine;
    throttle --> engine;
    engine --> speedSensor

```
