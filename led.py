from gpiozero import LED
from time import sleep
#import os

#os.system("node-red-stop")

# Define LED port on gpio 21
led = LED(17)   # Pin no. 40 gpio 21

try:
    while True:
        led.on()  # Turn LED ON
        print("LED ON")
        sleep(1)  # Wait 1 second
        
        led.off()  # Turn LED OFF
        print("LED OFF")
        sleep(1)  # Wait 1 second

except KeyboardInterrupt:
    print("\nExiting...")
    sleep(2)

led.close()
#print("Restarting Node-red")
#os.system("node-red-restart")
#sleep(2)
#print("Nodered restarted")