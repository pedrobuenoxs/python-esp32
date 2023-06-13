import serial
import time
import csv
from collections import deque

SERIAL_PORT = '/dev/ttyUSB1'
BAUD_RATE = 115200
MOVING_AVERAGE_SIZE = 10

class CustomSerial:
    def __init__(self, ser=serial.Serial(SERIAL_PORT, BAUD_RATE), moving_average_size=MOVING_AVERAGE_SIZE):
        """Initializes the CustomSerial object.

        Args:
            ser: The serial object to communicate with the device.
            moving_average_size: The size of the moving average window.
        """
        pass

    def _get_raw_data(self, sensor_type):
        """Retrieves and processes raw data from a specified sensor type.

        Args:
            sensor_type: The type of sensor ("ACCELEROMETER" or "GYROSCOPE").

        Returns:
            A list of data values.
        """
        pass

    def get_data(self, sensor_type):
        """Retrieves raw and moving average data from a specified sensor type.

        Args:
            sensor_type: The type of sensor ("ACCELEROMETER" or "GYROSCOPE").

        Returns:
            A tuple of two lists - raw data and moving average data.
        """
        pass

    def save_data(self):
        """Saves raw and moving average data from both sensors.
        """
        pass

    def download_csv(self, filename="sensor_data.csv"):
        """Writes all stored sensor data to a CSV file.

        Args:
            filename: The name of the CSV file.
        """
        pass

    def get_serial(self):
        """Returns the serial object.

        Returns:
            The serial object.
        """
        pass
