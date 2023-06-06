import serial
import time
import csv
from collections import deque


SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
MOVING_AVERAGE_SIZE = 10

class CustomSerial:
    """Handles serial communication with an accelerometer and gyroscope."""

    def __init__(self, ser=serial.Serial(SERIAL_PORT, BAUD_RATE), moving_average_size=MOVING_AVERAGE_SIZE):
        self.ser = ser
        self.moving_average_size = moving_average_size
        self.acc_data = [0, 0, 0]
        self.gyro_data = [0, 0, 0]
        self.acc_buffer = [deque(maxlen=self.moving_average_size) for _ in range(3)]
        self.gyro_buffer = [deque(maxlen=self.moving_average_size) for _ in range(3)]
        self.all_sensor_data = []

    def _get_raw_data(self, sensor_type):
        """Retrieves and processes raw data from a specified sensor type."""

        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if sensor_type.upper() in line:
                    clean_data = line.split()
                    data = [float(clean_data[i]) for i in range(3, 8, 2)]
                    return data
        except Exception as e:
            print(f"Error occurred while reading data: {e}")
            return [0, 0, 0]

    def get_data(self, sensor_type):
        """Retrieves raw and moving average data from a specified sensor type."""

        raw_data = self._get_raw_data(sensor_type)
        if raw_data is None:
            return None, None

        if sensor_type.upper() == "ACCELEROMETER":
            buffer = self.acc_buffer
            for i, value in enumerate(raw_data):
                buffer[i].append(value)
        else:  # Assume GYROSCOPE
            buffer = self.gyro_buffer
            for i, value in enumerate(raw_data):
                buffer[i].append(value)

        ma_data = [sum(d)/len(d) if len(d) > 0 else 0 for d in buffer]
        return raw_data, ma_data

    def save_data(self):
        """Saves raw and moving average data from both sensors."""

        acc_raw_data, acc_ma_data = self.get_data("ACCELEROMETER")
        gyro_raw_data, gyro_ma_data = self.get_data("GYROSCOPE")

        # Save data
        try:
            self.all_sensor_data.append([time.time()] + acc_raw_data + gyro_raw_data + acc_ma_data + gyro_ma_data)
        except:
            pass

    def download_csv(self, filename="sensor_data.csv"):
        """Writes all stored sensor data to a CSV file."""

        header = ["time", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z", "ma_acc_x", "ma_acc_y", "ma_acc_z", "ma_gyro_x", "ma_gyro_y", "ma_gyro_z"]
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for data in self.all_sensor_data:
                writer.writerow(data)

    def get_serial(self):
        """Returns the serial object."""

        return self.ser

