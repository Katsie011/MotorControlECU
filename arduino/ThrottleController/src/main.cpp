#include <Arduino.h>

// Constants
#define BAUD 9600
#define MINPOS 0
#define MAXPOS 150
#define MAX_FAILED_RECIEVES 20

#define FUEL_ENABLE_PIN PIN2
#define START_ENABLE_PIN PIN3
#define STARTER_DURATION_MS 1600

enum ECU_COMMAND
{
  STARTUP,
  STOP,
  FUEL,
  STARTER,
  THROTTLE,
};

// put function declarations here:
int checkPositionCommand();
int writeServoPosition(uint8_t pos);
void shutdown();
void blinkErrorUntilRestart();

// variables
uint8_t position = 0;
// uint8_t upperByte = 0;
// uint8_t lowerByte = 0;
uint8_t newPos = 0;

uint8_t failedRecieves = 0;
int timeMiliSinceLastRecieve = 0;

String message = "";
String command = "";
int data = 0;

/**
Arduino serial pins

Form Factor	RX	TX	RX1	TX1	RX2	TX2	RX3	TX3
MKR	        D0	D1
UNO	        D0	D1
Nano	      D0	D1
Mega	      D0	D1	D19	D18	D17	D16	D15	D14

*/

void setup()
{
  // put your setup code here, to run once:
  Serial1.begin(BAUD); // communication over RX/TX pins
}

void loop()
{
  // put your main code here, to run repeatedly:

  if (Serial.available() > 1)
  {
    timeMiliSinceLastRecieve = 0;
    processMessage();
  }
  else
  {
    // Serial not availible.
    // increase time since last transmission.
    // If we have lost connection, we need to do a safe shutdown
    timeMiliSinceLastRecieve += 100;

    if (timeMiliSinceLastRecieve / 1000 > 5)
    { // no recieve for 5 seconds
      shutdown();
    }
  }

  delay(100);
}

void processMessage()
{
  // read command from serial
  message = Serial1.readString();
  /**
   * LIST OF COMMANDS:
   *    > STARTUP
   *    > STOP
   *    > FUEL: 0/1      --  Fuel on or off
   *    > STARTER: x     --  run the starter for x ms
   *    > THROTTLE: x    --  move throttle to position x
   */

  // extract commands
  command = message.substring(0, message.indexOf('\n'));

  if (command.indexOf(":") > 0)
  {
    command = message.substring(0, message.indexOf(':'));
    command.toUpperCase();
    message = message.substring(message.indexOf(':') + 1);
    message.trim();
    data = message.toInt();
  }
  else
  {
    message.trim();
    message.toUpperCase();
    command = message;
  }

  if (command = "STARTUP")
  {
    Serial1.println("Starting");
    startup();
  }
  else if (command == "STOP")
  {
    Serial1.println("Stopping");
    shutdown();
  }
  else if (command == "FUEL")
  {
    Serial1.print("Setting fuel status to: ");
    Serial1.println(data > 0 ? 'on' : 'off' );
    digitalWrite(FUEL_ENABLE_PIN, data > 0 ? 1 : 0);
  }
  else if (command == "STARTER")
  {
    Serial1.print("Setting starter for: ");
    Serial1.print(data);
    Serial1.println("ms");

    digitalWrite(START_ENABLE_PIN,1);
    delay(data);
    digitalWrite(START_ENABLE_PIN,0);

  }
  else if (command == "THROTTLE")
  {
    Serial1.print("Setting throttle to: ");
    Serial1.print(data);
    Serial1.println("ms");
    runThrottle(data);
  }
  else
  {
    Serial1.print("Command ");
    Serial1.print(command);
    Serial1.println(" unrecognized.");

    // send message back saying the command is unrecognised.
    String help = "LIST OF COMMANDS:\n"
                  "#########################################"
                  "   * STARTUP\n"
                  "   * STOP\n" 
                  "   * FUEL: 0/1      --  Fuel on or off\n" 
                  "   * STARTER: x     --  run the starter for x ms\n" 
                  "   * THROTTLE: x    --  move throttle to position x\n";
    Serial1.print(help);
  }
}

int runThrottle(int position)
{
  // clean and process if needed
  if (newPos > MAXPOS || newPos < MINPOS)
  {
    return -1; // invalid byte
  }

  if (position < 0)
  {
    failedRecieves++;
  }
  else
  {
    failedRecieves = 0;
  }
  if (failedRecieves > MAX_FAILED_RECIEVES)
  {
    position = 0;
  }

  // write servo position
  writeServoPosition(position); // todo handle error
}

int writeServoPosition(uint8_t pos)
{
  // todo depending on servo interface
  return 0;
}

void startup()
{
  writeServoPosition((MINPOS + MAXPOS) / 2);

  // open fuel
  digitalWrite(FUEL_ENABLE_PIN, 0);

  // wait for fuel pump
  delay(1000);

  // start
  digitalWrite(START_ENABLE_PIN, 1);
  delay(STARTER_DURATION_MS);
  digitalWrite(START_ENABLE_PIN, 0);

  // check if we're running from the speed sensor
  // todo
}

void shutdown()
{
  writeServoPosition(MINPOS);
  // kill the fuel supply
  digitalWrite(FUEL_ENABLE_PIN, 0);
  blinkErrorUntilRestart();
}

void blinkErrorUntilRestart()
{
  // safe error state
  while (true)
  {
    digitalWrite(LED_BUILTIN, 1);
    delay(300);
    digitalWrite(LED_BUILTIN, 0);
    delay(300);
  }
}

int sendPosInt(uint8_t pos)
{
  // for transmitting large numbers
  Serial.write(highByte(pos));
  Serial.write(lowByte(pos));
}