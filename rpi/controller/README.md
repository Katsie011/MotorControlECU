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


# Setup:
A great resource and al in one builder for the docker containers we need is here:  https://learnembeddedsystems.co.uk/easy-raspberry-pi-iot-server

Create the database: 
``` bash
docker exec -it influxdb influx
CREATE DATABASE REX
quit
```

# Test Influx install:
``` bash
curl -i -XPOST 'http://4qtrexpi.local:8086/write?db=REX' --data-binary 'test,tag1=web_test,tag_n=post value=0.3'

```

Check the value was inserted with:
``` bash
docker exec -it influxdb influx
USE REX
show measurements
```

# Loging into Grafana:
```bash
http://4qtrexpi.home:3000/login 
# or 
http://4qtrexpi.local:3000/login
```