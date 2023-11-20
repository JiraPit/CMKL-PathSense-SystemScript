import threading

class CameraThreader(threading.Thread):
    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.last_frame = None
        self.running = True
        self.frame_ready = threading.Condition()

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if frame is not None and frame.size > 0:
                    with self.frame_ready:
                        self.last_frame = frame
                        self.frame_ready.notify()
            else:
                self.cap.release()
                self.running = False

    def read_last_frame(self):
        with self.frame_ready:
            self.frame_ready.wait()
            return self.running, self.last_frame

    def stop(self):
        self.cap.release()
        self.running = False
