# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyautogui",
#     "pillow",
#     "opencv-python",
#     "numpy",
#     "keyboard",
#     "click",
# ]
# ///

import base64
import io
import json
import os
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
import time
import click
import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import Image

# Placeholder base64 images - replace with actual button images later
LAUNCHER_IMG = "data:image/png;base64,placeholder_for_launcher_button"
WEBSITE_IMG = "data:image/jpeg;base64,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"

@dataclass
class ButtonData:
    image: str
    region: Tuple[int, int, int, int]
    click_offset: Tuple[int, int]
    timestamp: float

@dataclass
class ButtonMatch:
    region: Tuple[int, int, int, int]
    confidence: float
    screenshot: np.ndarray

class CalibrationManager:
    def __init__(self, config_path: str = "button_calibration.json"):
        self.config_path = config_path
        self.calibration_data: Dict[str, ButtonData] = {}
        self.load_config()

    def load_config(self) -> None:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.calibration_data = {
                    k: ButtonData(**v) for k, v in data.items()
                }

    def save_config(self) -> None:
        with open(self.config_path, 'w') as f:
            json.dump(self.calibration_data, f, default=lambda x: x.__dict__)

    def capture_button(self, button_type: str) -> Optional[ButtonData]:
        print(f"\nLooking for {button_type} button...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        
        matches = self._find_button_candidates(screenshot_np)
        if not matches:
            print("No button candidates found. Try adjusting window position.")
            return None

        selected_match = self._select_button_match(matches[:5])  # Only show top 5 candidates
        if not selected_match:
            return None

        button_region = selected_match.region
        click_pos = self._get_click_position(button_region)
        if not click_pos:
            return None

        button_img = selected_match.screenshot[
            button_region[1]:button_region[1]+button_region[3], 
            button_region[0]:button_region[0]+button_region[2]
        ]
        
        return ButtonData(
            image=self._np_to_base64(button_img),
            region=button_region,
            click_offset=click_pos,
            timestamp=time.time()
        )

    def _find_button_candidates(self, screenshot: np.ndarray) -> List[ButtonMatch]:
        matches = []
        gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        
        # Simple edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter for rectangular shapes
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size and aspect ratio
            if w > 20 and h > 20:  # Minimum size
                aspect_ratio = w / h
                if 1.5 < aspect_ratio < 5:  # Typical button aspect ratios
                    area = cv2.contourArea(contour)
                    rect_area = w * h
                    extent = area / rect_area  # How rectangular is it
                    
                    if extent > 0.7:  # Must be fairly rectangular
                        matches.append(ButtonMatch(
                            region=(x, y, w, h),
                            confidence=extent,
                            screenshot=screenshot
                        ))
        
        return sorted(matches, key=lambda x: x.confidence, reverse=True)
    
    def _non_max_suppression(self, matches: List[ButtonMatch], overlap_thresh: float = 0.3) -> List[ButtonMatch]:
        if not matches:
            return []
            
        # Convert regions to format needed for NMS
        boxes = np.array([[m.region[0], m.region[1], 
                          m.region[0] + m.region[2], 
                          m.region[1] + m.region[3]] for m in matches])
        scores = np.array([m.confidence for m in matches])
        
        # Calculate areas
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        
        # Sort by confidence
        idxs = np.argsort(scores)
        pick = []
        
        while len(idxs) > 0:
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            
            # Find overlapping boxes
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])
            
            # Calculate overlap
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            overlap = (w * h) / areas[idxs[:last]]
            
            # Delete overlapping boxes
            idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
        
        return [matches[i] for i in pick]

    def _select_button_match(self, matches: List[ButtonMatch]) -> Optional[ButtonMatch]:
        if not matches:
            return None
            
        preview = matches[0].screenshot.copy()
        
        # Draw all candidates with numbers
        for i, match in enumerate(matches):
            x, y, w, h = match.region
            cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"{i + 1}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            (label_w, label_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
            
            cv2.rectangle(preview, 
                         (x, y - label_h - 10), 
                         (x + label_w + 10, y), 
                         (255, 255, 255), 
                         -1)
            cv2.putText(preview, 
                        label,
                        (x + 5, y - 5),
                        font,
                        font_scale,
                        (0, 0, 0),
                        thickness)
        
        window_name = "Button Candidates"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        screen_height = preview.shape[0]
        window_height = int(screen_height * 0.8)
        window_width = int(window_height * (preview.shape[1] / screen_height))
        cv2.resizeWindow(window_name, window_width, window_height)
        cv2.imshow(window_name, preview)
        cv2.waitKey(100)
        
        print("\nButton candidates found:")
        for i, match in enumerate(matches):
            print(f"{i + 1}: Confidence {match.confidence:.2f}")
        
        while True:
            try:
                choice = input("\nEnter number of correct button (or 0 to cancel): ")
                if choice == "0":
                    cv2.destroyWindow(window_name)
                    cv2.waitKey(1)
                    return None
                index = int(choice) - 1
                if 0 <= index < len(matches):
                    cv2.destroyWindow(window_name)
                    cv2.waitKey(1)
                    return matches[index]
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except cv2.error:
                print("Window closed. Cancelling selection.")
                return None

    def _get_click_position(self, region: Tuple[int, int, int, int]) -> Optional[Tuple[int, int]]:
        x, y, w, h = region
        return (x + w // 2, y + h // 2)  # Always use center of button

    @staticmethod
    def _np_to_base64(image: np.ndarray) -> str:
        """Convert numpy array image to base64 string."""
        pil_img = Image.fromarray(image)
        img_byte_arr = io.BytesIO()
        pil_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return f"data:image/png;base64,{base64.b64encode(img_byte_arr).decode()}"

    def run_calibration(self, button_type: str) -> None:
        print(f"\nCalibrating {button_type} button")
        button_data = self.capture_button(button_type)
        if button_data:
            self.calibration_data[button_type] = button_data
            print(f"Successfully captured {button_type} button")
            self.save_config()
        
        # Start auto-clicking after calibration
        if button_type in self.calibration_data:
            button_img = base64_to_image(self.calibration_data[button_type].image)
            print("Starting auto-clicker. Press Ctrl+C to exit.")
            while True:
                find_and_click(button_img, button_type)

def base64_to_image(base64_str: str) -> Image.Image:
    img_data = base64.b64decode(base64_str.split(',')[1])
    return Image.open(io.BytesIO(img_data))

def find_and_click(image: Image.Image, name: str, threshold: float = 0.8) -> None:
    try:
        location = pyautogui.locateOnScreen(image, confidence=threshold)
        if location:
            pyautogui.click(location.left + location.width // 2, 
                          location.top + location.height // 2)
            print(f"Found and clicked {name}")
            time.sleep(2)
    except pyautogui.ImageNotFoundException:
        print(f"{name} not found, waiting...")
        time.sleep(3)

@click.command()
@click.option('-c', '--calibrate', help='Run calibration mode for specific button')
@click.option('-l', '--load-config', is_flag=True, help='Load calibrated button data')
def main(calibrate: str, load_config: bool) -> None:
    pyautogui.FAILSAFE = False
    
    if calibrate:
        calibration = CalibrationManager()
        calibration.run_calibration(calibrate)
        return
        
    if load_config:
        calibration = CalibrationManager()
        if not calibration.calibration_data:
            print("No calibration data found. Run with --calibrate first.")
            return
        
        print("Starting auto-clicker with calibrated buttons. Press Ctrl+C to exit.")
        while True:
            for button_type, data in calibration.calibration_data.items():
                button_img = base64_to_image(data.image)
                find_and_click(button_img, button_type)
    else:
        # Use default images
        print("Starting auto-clicker with default buttons. Press Ctrl+C to exit.")
        while True:
            launcher_img = base64_to_image(LAUNCHER_IMG)
            website_img = base64_to_image(WEBSITE_IMG)
            find_and_click(launcher_img, "launcher")
            find_and_click(website_img, "website")

if __name__ == "__main__":
    main()
