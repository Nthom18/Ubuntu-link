#include <wiringPi.h>
int main (void)
{
  int red = 0;
  int yellow = 2;
  int green = 3;
  int pin = 1;

  wiringPiSetup () ;
  pinMode (pin, OUTPUT) ;
  for (;;)
  {
    digitalWrite (pin, HIGH); 
    delay (500);
    digitalWrite (pin,  LOW);
    delay (500);
  }
  return 0 ;
}
