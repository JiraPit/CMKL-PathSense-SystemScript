import subprocess
from dependencies.server_interface import ServerInterface

class BluetoothInterface:
    def __init__(self):
        self.server = ServerInterface()

    # Turn Bluetooth on and make it discoverable
    def turn_on(self):
        cmd = (
            "echo -e 'power on\n"
            "agent NoInputNoOutput\n"
            "default-agent\n"
            "discoverable on\n"
            "pairable on\n"
            "trust *\n"
            "quit'"
            " | sudo bluetoothctl"
            )
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()

    # Turn Bluetooth off
    def turn_off(self):
        cmd = "echo -e 'power off\nquit' | sudo bluetoothctl"
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()
    
    # Get client device address
    def get_client_address(self):
        try:
            cmd = "echo -e 'devices\nquit' | sudo bluetoothctl"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            out, _ = process.communicate()
            lines = out.decode('utf-8').split('\n')
            for line in lines:
                if line.startswith('Device'):
                    address = line.split()[1]
                    break
            return address
        except Exception as e:
            self.server.log(e, mode="error")
            return None