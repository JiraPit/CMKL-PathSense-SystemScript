import threading
import time

class CameraThreader(threading.Thread):
    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.last_frame = None
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if frame is not None:
                    self.last_frame = frame
            else:
                self.stop()
            time.sleep(0.05)
    
    def read_last_frame(self):
        return self.running, self.last_frame

    def stop(self):
        self.running = False