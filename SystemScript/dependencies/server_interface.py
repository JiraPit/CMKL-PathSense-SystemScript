import requests
import cv2
from dependencies.configuration import LTOKEN, DID

class ServerInterface:

    def __init__(self):
        self.server_root = "https://ai-model-server-55few4lhsq-as.a.run.app"
        self.headers = {'link-token': LTOKEN(), 'did': DID()}

    
    # Send image to server for path classification
    def send_to_server(self,image):
        
        # Encode image to JPEG
        _, encoded = cv2.imencode('.jpg', image)

        # Send image to server
        response = requests.post(
            f'{self.server_root}/path-classification', 
            files={'file': ('image.jpg', encoded.tobytes(), 'image/jpeg')},
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            self.log(f"An error occurred while calling [send_to_server]: {response.status_code}", mode="error")
            return None

    # Get camera status from server
    def get_camera_status(self):

        # Get camera status from server
        response = requests.get(
            f'{self.server_root}/camera-status',
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json()['status']
        else:
            self.log(f"An error occurred while calling [get_camera_status]: {response.status_code}", mode="error")
            return False

    # Log error to server
    def log(self,message,mode='info'):

        # Print error to console
        print(f"Logging: {message}")

        # Send error to server
        requests.post(
            f'{self.server_root}/log',
            json={'message': message, 'mode': mode},
            headers=self.headers,
        )