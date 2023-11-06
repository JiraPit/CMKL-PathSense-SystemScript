import bluetooth
from dependencies.server_interface import ServerInterface

class BluetoothInterface:
    def __init__(self):
        self.__server = ServerInterface()
        self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.__client_sock = None

    # Turn Bluetooth on and make it discoverable
    def turn_on(self):
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.__socket.bind(("", bluetooth.PORT_ANY))
        self.__socket.listen(1)
        bluetooth.advertise_service(
            self.__socket, 
            "PathSense Bag",
        )

    # Turn Bluetooth off
    def turn_off(self):
        self.__socket.close()

    # Wait for connection from mobile app and return address
    def wait_for_connection(self):
        self.__client_sock, client_info = self.__socket.accept()
        self.__server.log(f"Accepted connection from {client_info}", mode="info")

    # Send a message to the client
    def send_message(self, message):
        if self.__client_sock is not None:
            try:
                self.__client_sock.send(message)
            except Exception as e:
                self.__server.log(e, mode="error")
        else:
            self.__server.log("Can't send message because no client connected", mode="error")
    
    # Receive a message from the client
    def receive_message(self):
        if self.__client_sock is not None:
            message = self.__client_sock.recv(1024)
            return message.decode('utf-8')
        else:
            self.__server.log("Can't receive message because no client connected", mode="error")
