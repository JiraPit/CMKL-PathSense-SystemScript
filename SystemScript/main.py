import cv2
import time
import argparse

from dependencies.server_interface import ServerInterface
from dependencies.bluetooth_interface import BluetoothInterface
import dependencies.configuration as conf

def main(args):

    # Initialize server and bluetooth interfaces
    server = ServerInterface()
    bluetooth = BluetoothInterface()

    # Validate tokens and restore if invalid
    conf.restore() if not conf.is_valid() else None

    # If still invalid, turn on bluetooth start pairing process
    while not conf.is_valid():
        server.log("Starting pairing process.", mode="info")
        bluetooth.turn_on()
        bluetooth.wait_for_connection()

        # Send DID to client
        bluetooth.send_message(conf.DID())

        # Recieve link token and set it in configuration
        conf.set_ltoken("55555")

        # Close bluetooth connection
        bluetooth.turn_off()

        # If still invalid, try again
        if not conf.is_valid():
            server.log("Invalid token. Please try again.", mode="error")
        else:
            server.log("Token successfully validated.", mode="info")
    
    server.log("Starting main life cycle.", mode="info")

    # Keep alive until forced to close
    while True:
        try:

            # Open camera
            cap = cv2.VideoCapture(args.device)

            # Set camera resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

            try:

                # Keep capturing images until error occurs
                while True:

                    # Check if camera is still active on server
                    if not server.get_camera_status():
                        break

                    # Capture image
                    ret, frame = cap.read()

                    # If no image captured, break out and try again
                    if not ret:
                        break

                    # Send image to server for path classification
                    server.send_to_server(frame)
                    
                    # Delay before capturing next image
                    time.sleep(args.delay)
            
            # If error occurs, try again
            except Exception as e:
                server.log(e, mode="error")

            # Close camera before trying again in 3x the delay time
            finally:
                if cap != None:
                    cap.release()
                cap = None
                time.sleep(5)

        # If forced to close, close camera and exit permanently
        finally:
            if cap != None:
                cap.release()
            server.log("Permanently closed due to forced exit.", mode="info")
            break

# Format device argument to be either an integer or string
def valid_device(device):
    try:
        return int(device)
    except ValueError:
        return str(device)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture images every few seconds.')
    parser.add_argument('--delay', type=float, default=2, help='Delay time in seconds between capturing images.')
    parser.add_argument('--device', type=valid_device, required=True, help='Index or path of the camera to use for capturing images.')
    args = parser.parse_args()
    main(args)