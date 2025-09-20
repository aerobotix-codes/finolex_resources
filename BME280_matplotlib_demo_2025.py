#install matplotlib library : pip install matplotlib --break-system-packages
import board
import busio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque      # deque for handling elements in collection queue from both ends
import time
import csv
import os
from adafruit_bme280 import basic

# === Sensor Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = basic.Adafruit_BME280_I2C(i2c, address=0x76)  # change to 0x77 if needed

# Set sea level pressure (needed for accurate altitude)
bme280.sea_level_pressure = 1013.25  # You can adjust to your local value

# === Data Buffers ===
max_len = 50
temperature_data = deque([0]*max_len, maxlen=max_len)
humidity_data = deque([0]*max_len, maxlen=max_len)
pressure_data = deque([0]*max_len, maxlen=max_len)
altitude_data = deque([0]*max_len, maxlen=max_len)
x_data = deque([0]*max_len, maxlen=max_len)

start_time = time.time()

# === CSV Setup ===
csv_file = "bme280_real_data.csv"
write_header = not os.path.exists(csv_file)

if write_header:
    with open(csv_file, mode='a', newline='') as file:         # mode 'a' is to keep appending values in file
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Temperature (°C)", "Humidity (%)", "Pressure (hPa)", "Altitude (m)"])

# === Matplotlib Plot Setup ===
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 10))       # 4 rows , 1 Column, 10 inch x 10 inch figure
fig.suptitle('Live BME280 Sensor Data (Temp, Humidity, Pressure, Altitude)')

def animate(i):
    # === Read Sensor ===
    temperature = round(bme280.temperature, 2)
    humidity = round(bme280.humidity, 2)
    pressure = round(bme280.pressure, 2)
    altitude = round(bme280.altitude, 2)
    t = round(time.time() - start_time, 1)

    # === Store in Buffers ===
    x_data.append(t)
    temperature_data.append(temperature)
    humidity_data.append(humidity)
    pressure_data.append(pressure)
    altitude_data.append(altitude)

    # === Plot Temp ===
    ax1.clear(); 
    ax1.plot(x_data, temperature_data, 'r'); 
    ax1.set_ylabel('Temp (°C)')
    
    # === Plot Humidity ===
    ax2.clear(); 
    ax2.plot(x_data, humidity_data, 'g'); 
    ax2.set_ylabel('Humidity (%)')
    
    # === Plot Pressure ===
    ax3.clear(); 
    ax3.plot(x_data, pressure_data, 'b'); 
    ax3.set_ylabel('Pressure (hPa)')
    
    # === Plot Altitude ===
    ax4.clear(); 
    ax4.plot(x_data, altitude_data, 'm'); 
    ax4.set_ylabel('Altitude (m)')
    
    ax4.set_xlabel('Time (s)')

    for ax in (ax1, ax2, ax3, ax4):
        ax.grid(True)

    # === Write to CSV ===
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([t, temperature, humidity, pressure, altitude])

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.tight_layout()
plt.show()
