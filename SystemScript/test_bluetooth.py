from dependencies.bluetooth_interface_cmd import BluetoothInterface
import time

def main():
    bluetooth = BluetoothInterface()

    bluetooth.turn_on()

    while True:
        address = bluetooth.get_client_address()
        print(address)
        time.sleep(2)
