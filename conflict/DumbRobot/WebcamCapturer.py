import os
import glob
import cv2

class WebcamCapturer:
    def __init__(self, device_index=0, capture_interval=5, images_folder="CapturedImages"):
        """
        device_index: The index of the webcam (0 for default camera)
        capture_interval: The number of seconds between captures
        images_folder: Path to the folder where captured images are stored
        """
        self.device_index = device_index
        self.capture_interval = capture_interval
        self.images_folder = images_folder
        os.makedirs(self.images_folder, exist_ok=True)  # Ensure folder exists

        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            raise ValueError("Unable to open the webcam")

    def clear_old_images(self):
        # Delete all images in the images_folder
        for file_path in glob.glob(os.path.join(self.images_folder, "*")):
            os.remove(file_path)

    def capture_frame(self, output_prefix="frame", output_suffix="999", on_image_captured=None):
        """
        Capture a single frame from the webcam and save it as an image file.
        
        on_image_captured: Callback function that will be triggered with the path of each captured image.
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from webcam.")
            return
        filename = f"{output_prefix}_{output_suffix}.jpg"
        output_path = os.path.join(self.images_folder, filename)
        cv2.imwrite(output_path, frame)
        print(f"Saved {output_path}")
        if on_image_captured is not None:
            on_image_captured(output_path)

    def release(self):
        self.cap.release()