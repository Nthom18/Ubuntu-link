#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

// Prototype
void switchLED();

// Defines
#define WAIT 1000

// Global declares
int red = 17;       	//GPIO 17
int yellow = 27;      	//GPIO 27
int green = 23;       	//GPIO 23
int button = 24;	//GPIO 24

int main ()
{
  //Setup
  wiringPiSetupGpio (); pinMode(red, OUTPUT); pinMode(yellow, OUTPUT); pinMode(green, OUTPUT);

  // Configure button as OUTPUT and set to HIGH. Press is detected if the pin is open circuited
  pinMode(button, OUTPUT); digitalWrite(button, HIGH);

  // Light green LED
  digitalWrite(green, HIGH);

  // Open server and write to text-file
  int net;
  system("touch received.txt");
  system("> received.txt");
  system("socat -v tcp-listen:8080,fork,reuseaddr OPEN:received.txt,creat,append &");

  // Main loop
  for (;;)
  {
    // Update and read from received.txt
    FILE* received = fopen("received.txt", "r");
    fscanf(received, "%d", &net);

    // Switch if input is received
    if ((!digitalRead(button)) | (net == 1))
    {
      system("> received.txt");
      net = 0;
      switchLED();
    }
    fclose(received);
  }
  return 0;
}

/****************************************** FUNCTIONS *********************************************/

void switchLED()
{
  int isGreen = digitalRead(green);
  int isRed = digitalRead(red);

  digitalWrite(red, LOW); digitalWrite(green, LOW);

  if (isGreen)
  {
    digitalWrite(yellow, HIGH);
    delay(WAIT);
    digitalWrite(yellow, LOW);
    digitalWrite(red, HIGH);
  }    
  else if (isRed)
  {
    digitalWrite(red, HIGH);
    digitalWrite(yellow, HIGH); 
    delay(WAIT);
    digitalWrite(red, LOW);
    digitalWrite(yellow, LOW); 
    digitalWrite(green, HIGH);
  }

  delay(WAIT);
}
