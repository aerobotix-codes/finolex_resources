from gpiozero import LED
from time import sleep
from espeak import espeak

# Define LED port on gpio 21
led = LED(17)   # Pin no. 40 gpio 21
sleep(1)
espeak.synth("welcome to jarvis system")
sleep(3)
try:
    while True:
        led.on()  # Turn LED ON
        print("LED ON")
        espeak.synth("Lights ON")
        sleep(3)  # Wait 1 second
        
        led.off()  # Turn LED OFF
        print("LED OFF")
        espeak.synth("Lights OF")
        sleep(3)  # Wait 1 second

except KeyboardInterrupt:
    print("\nExiting...")
    sleep(2)
    espeak.synth("Bye Bye")
    sleep(2)

led.close()
