from custom_serial import CustomSerial
from game import SensorGame


def main():
    custom_serial = CustomSerial()
    game = SensorGame(custom_serial)
    game.run()


if __name__ == "__main__":
    main()
