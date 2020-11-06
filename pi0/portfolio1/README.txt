
The LED's and the button are connected to the following pins:

red: 	GPIO 17
yellow: GPIO 27
green:	GPIO 23
button: GPIO 24

To activate the trigger via the network, send '1' to the device via socat:
echo 1 | socat - tcp:localhost:8080