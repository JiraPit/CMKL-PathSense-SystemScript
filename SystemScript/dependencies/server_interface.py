import requests
import cv2
from dependencies.configuration import LTOKEN, DID

class ServerInterface:

    def __init__(self):
        self.server_root = "https://ai-model-server-55few4lhsq-as.a.run.app"
        self.headers = {'link-token': LTOKEN(), 'did': DID()}
    
    # Send image to server for path classification
    def process(self,image):
        # Encode image to JPEG
        _, encoded = cv2.imencode('.jpg', image)

        # Send image to server
        response = requests.post(
            f'{self.server_root}/process', 
            files={'file': ('image.jpg', encoded.tobytes(), 'image/jpeg')},
            headers=self.headers,
        )
        if response.status_code == 200:
            return dict(response.json())
        else:
            self.log(f"[process] {response.status_code}", mode="error")
            return None

    # Get camera status from server
    def get_camera_status(self):
        # Get camera status from server
        response = requests.get(
            f'{self.server_root}/camera-status',
            headers=self.headers,
        )

        # Check if response is valid
        if response.status_code == 200:
            result = response.json()

            # Check if response is successful
            if result['status'] == 'success':
                return result['result']
            else:
                self.log(f"[get_camera_status] {result['result']}", mode="error")
                return False
        else:
            self.log(f"[get_camera_status] {response.status_code}", mode="error")
            return False

    # Log error to server
    def log(self,message,mode='info'):
        try:
            # Print error to console
            print(f"Logging: {message}")

            # Send error to server
            requests.post(
                f'{self.server_root}/client-log',
                json={'message': message, 'mode': mode},
                headers=self.headers,
            )
        except:
            return