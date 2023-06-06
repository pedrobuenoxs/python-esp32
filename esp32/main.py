from machine import Pin
from esp32.mpu6050 import MPU6050
import ustruct

sda = Pin(21)
scl = Pin(22)
bus = 1 # or whichever bus your device is connected to

sensor = MPU6050(bus, sda, scl)

def run():
    while True:
        try:
            sensor.print_data()
        except Exception as e:
            print(e)
            pass    

if __name__ == "__main__":
    run()