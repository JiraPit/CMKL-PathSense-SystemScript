from dependencies.bluetooth_interface_cmd import BluetoothInterface
import time

def main():
    bluetooth = BluetoothInterface()
    print("Turning on bluetooth...")
    bluetooth.turn_on()
    while True:
        print("Getting client address...")
        address = bluetooth.get_client_address()
        print(address)
        time.sleep(2)

if __name__ == "__main__":
    main()
