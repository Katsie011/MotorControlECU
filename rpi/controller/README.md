# Code to run the controller for the Range Extender

Tasks for the controller
- [ ] Read in Power command from the VCU via a can message
  - [ ] Connect to the CAN network on startup
  - [ ] Make sure we have the right CAN ID
  - [ ] Listen for the command from the VCU to startup and give power
- [ ] Tell the ECU to start
- [ ] Calculate the optimal setpoints in terms of speed and torque to pull the require power safely and efficiently. 
- [ ] Once ICE is ready, ramp up to the required setpoint
  - [ ] Increase ICE speed
  - [ ] Increase torque, being careful to not stall the motor. 
  - [ ] Initally use PID, later work with MPC. Bonus points if we can use DL