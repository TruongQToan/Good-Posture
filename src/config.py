class CameraConfig:
    def __init__(self):
        self.fps = 30
        self.cam_num = 0
        self.camera_size = (400, 400)

class Config:
    def __init__(self):
        self.style = "Fusion"
        self.algorithms = ["open_pose", "haar_detection"]
        self.camera_config = CameraConfig()
        self.window_size = (640, 480)
