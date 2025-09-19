import time
import board
import busio
from adafruit_bme280 import basic

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create BME280 object
bme280 = basic.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: Set the sea level pressure in hPa (use your local sea level pressure)
bme280.sea_level_pressure = 1013.25  # Sea level pressure in hPa

def get_sensor_data():
    # Get temperature, humidity, pressure, and altitude
    temperature = bme280.temperature  # Temperature in Celsius
    humidity = bme280.relative_humidity  # Humidity in %
    pressure = bme280.pressure  # Pressure in hPa
    altitude = bme280.altitude  # Altitude in meters

    return temperature, humidity, pressure, altitude

try:
    while True:
        temperature, humidity, pressure, altitude = get_sensor_data()
        
        # Print the sensor values
        print("\n************************")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Altitude: {altitude:.2f} meters")
        print("************************")
        time.sleep(2)  # Wait for 2 seconds before reading again

except KeyboardInterrupt:
        
        print("\nexiting...")
        time.sleep(1)  # Wait for 2 seconds before reading again