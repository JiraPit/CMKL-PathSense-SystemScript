import cv2
import time
import re
import subprocess

from dependencies.server_interface import ServerInterface
from dependencies.bluetooth_interface import BluetoothInterface
import dependencies.configuration as conf

def main():
    # Initialize server and bluetooth interfaces
    server = ServerInterface()
    bluetooth = BluetoothInterface()

    # Validate tokens and restore if invalid
    print("Validating tokens...")
    conf.restore() if not conf.is_valid() else None

    # If still invalid, turn on bluetooth start pairing process
    while not conf.is_valid():
        print("Invalid token. Turning on bluetooth and waiting for connection...")
        bluetooth.turn_on()
        bluetooth.wait_for_connection()

        # Send DID to client
        print("Bluetooth connected. Sending DID...")
        bluetooth.send_message(conf.DID())

        # Recieve link token and set it in configuration
        print("Link token recieved. Finishing pairing process...")
        conf.set_ltoken("289788498")

        # Close bluetooth connection
        bluetooth.turn_off()

        # If still invalid, try again
        if not conf.is_valid():
            server.log("[main] Invalid token. Trying again.", mode="error")
    
    # Keep alive until forced to close
    try:
        while True:
            # Find and open camera
            cap = None
            camera = find_camera_device()
            print(f"Opening camera at /dev/video{camera}...")
            marker = time.time()
            if camera is None:
                server.log("[main] No camera found.", mode="error")
                break
            else:
                cap = cv2.VideoCapture(camera)
            print(f"Opening camera took {time.time() - marker:.6f} seconds")

            # Set camera resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

            try:
                while True:
                    # Check if camera is still active on server
                    print("Checking camera status...")
                    marker = time.time()
                    status = server.get_camera_status()
                    if not status:
                        print("Camera is not active on server. Waiting for server to activate camera.")
                        break
                    print(f"Get camera status took {time.time() - marker:.6f} seconds")

                    # Capture image
                    print("Capturing image...")
                    marker = time.time()
                    ret, frame = cap.read()
                    if not ret: 
                        break
                    print(f"Capture image took {time.time() - marker:.6f} seconds")

                    # Send image to server for path classification
                    print("Sending image to server...")
                    marker = time.time()
                    result = server.process(frame)
                    print(f"Sending image to server took {time.time() - marker:.6f} seconds")
                    print(f"Result: {[key for key, value in result["result"].items() if value == 1]}")

                    # Delay before capturing next image
                    print("Waiting for 2 seconds...\n\n")
                    time.sleep(2)
            
            # If forced to close, close camera and exit
            except KeyboardInterrupt:
                print("Keyboard interrupted")
                break
            
            # If error occurs, try again
            except Exception as e:
                server.log("[main] " + str(e), mode="error")

            # Close camera before trying again in 5 seconds
            finally:
                if cap != None:
                    cap.release()
                cap = None
                time.sleep(5)
        
    except Exception as e:
        server.log("[main] " + str(e), mode="error")

    # If forced to close, close camera and exit permanently
    finally:
        if cap != None:
            cap.release()
        print("force closed")

# Find the camera device
def find_camera_device():
    # Iterate through the first 10 video devices
    for i in range(10):
        try:
            # Run v4l2-ctl to find the formats supported by the device
            output = subprocess.check_output(["v4l2-ctl", "--device=/dev/video" + str(i), "--list-formats"])
        except subprocess.CalledProcessError:
            # If the device does not exist, skip to the next one
            continue

        # Check if the device supports a streaming video format (e.g., 'YUYV', 'MJPG', 'H264')
        if re.search(b'\'MJPG\'', output):
            return i

    # If no suitable device is found, return None
    return None

if __name__ == "__main__":
    main()