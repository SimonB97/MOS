# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyautogui",
#     "pillow",
#     "opencv-python",
#     "pytesseract",
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
import pytesseract
import pyautogui
from PIL import Image

LAUNCHER_IMG = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAZCAYAAABuKkPfAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKpSURBVFhH7VbfaxNBEPav66v/gCD4Jr4ogj8qilDEF6U+9M2KVoVam1q1SpE+RBppTbXFSpqkl2Qvyd0l9zP/wjjfnHdc9VpSvILQffi43ZnZnZlvZ2fvTGN6gk47NAkMTQJDk8DQJDA0CQxNAuNQEty9dRqNRjGikILuHpnvpnJti4T5fopCuy3fPP1x0Xl1hYJek6zybK4eOJIEX/2UcWf+MnnNTQodk9TSrb9si8R/SwLQfnmJgv4+DbZX0rm3X5UqiUKf3Npnaj29QM7mAjttUPvFRTKenOdxnQY7H2VNf21GErTKjyUwt7FBUeDJHm6tTM2ZswdIwNyplijyh1yREVdjPa1G6Ia7a+IbOt+skXp9TXTdD/f5wFS8pm/IuBASUlnnRzoO7Bap0mTqFAR1V+5JEpD1Vh9Q5DmyjyT0bVnGavGG2GAvkGlV5igc9sQ+SwICj1ybrPVnMenNr0xETciFTNZ8eiQxiH8mG+TjENzGFzJmz5FdeR7vUSgJLOssXBUC7I35VIcAcOrqzW0JAjqnuiSJygku35EkYPdniUrinBDmWRLceoW81nbqo7f6kMKBKV8kqxavpzrYIr74QGIbyAu9DqmMk8oGneiQMIKHU9gBnrElZPjtnd/XpC5rxiUB/rFP4iNrJ32q9Z2vUpA2cNhCBxvYYs2J9QSpBMuQUkv0SSWgVCHHXURF4HpAhzuLuSrdPF4lcPUkPrKVgDhQjebbu6JLCDuxSsh7HaDP6wnQofSRFK4BSEFDRHPDycl+Y5KA+WE9AU0RpEOeJI6YpBmzTWE9Ifuf4KvdA/8JElTO6wCdBMIBIlCxRbPiKkJjxHxcEo56HfASIFnIsRaVljTt5FD++XU4TdAkMDQJDE0CQ5PA0CQwNAkMTQJDkzA9Qb8ALwHi52gP8aUAAAAASUVORK5CYII="
WEBSITE_IMG = "data:image/jpeg;base64,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"

@dataclass
class ButtonFeatures:
    template: np.ndarray
    edges: np.ndarray
    text: str
    color_hist: np.ndarray
    click_offset: Tuple[int, int]

@dataclass
class CalibrationData:
    features: List[ButtonFeatures]
    confidence_threshold: float
    success_rate: float
    timestamp: float

@dataclass
class ButtonData:
    image: str
    text: str
    region: Tuple[int, int, int, int]
    click_offset: Tuple[int, int]
    timestamp: float

class CalibrationManager:
    def __init__(self, config_path: str = "button_calibration.json"):
        self.config_path = config_path
        self.calibration_data: Dict[str, ButtonData] = {}
        self.current_samples: Dict[str, List[ButtonFeatures]] = {"launcher": [], "website": []}
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

    def extract_features(self, image: np.ndarray, click_pos: Tuple[int, int], region: Tuple[int, int, int, int]) -> ButtonFeatures:
        x, y, w, h = region
        button_img = image[y:y+h, x:x+w]
        gray = cv2.cvtColor(button_img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        hist = cv2.calcHist([button_img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        text = pytesseract.image_to_string(button_img).strip()
        click_offset = (click_pos[0] - x, click_pos[1] - y)
        return ButtonFeatures(template=button_img, edges=edges, text=text, color_hist=hist, click_offset=click_offset)

    def analyze_samples(self, button_type: str) -> CalibrationData:
        samples = self.current_samples[button_type]
        if not samples:
            return None
        confidence = 0.8
        text_similarity = self._calculate_text_similarity([s.text for s in samples])
        color_similarity = self._calculate_color_similarity([s.color_hist for s in samples])
        edge_similarity = self._calculate_edge_similarity([s.edges for s in samples])
        confidence *= (text_similarity + color_similarity + edge_similarity) / 3
        confidence = max(confidence, 0.6)
        return CalibrationData(features=samples, confidence_threshold=confidence, success_rate=1.0, timestamp=time.time())

    def find_button(self, screen: np.ndarray, button_type: str) -> Optional[Tuple[Tuple[int, int, int, int], float]]:
        print(f"Looking for {button_type} button...")
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Button Found", f"Found potential {button_type} button", duration=3, threaded=True)

    def _calculate_text_similarity(self, texts: List[str]) -> float:
        if not texts:
            return 0
        base = texts[0].lower()
        similarities = [self._string_similarity(base, t.lower()) for t in texts[1:]]
        return sum(similarities) / len(similarities) if similarities else 1

    def _calculate_color_similarity(self, hists: List[np.ndarray]) -> float:
        if not hists:
            return 0
        base = hists[0]
        similarities = [cv2.compareHist(base, h, cv2.HISTCMP_CORREL) for h in hists[1:]]
        return sum(similarities) / len(similarities) if similarities else 1

    def _calculate_edge_similarity(self, edges: List[np.ndarray]) -> float:
        if not edges:
            return 0
        base = edges[0]
        similarities = [self._edge_similarity(base, e) for e in edges[1:]]
        return sum(similarities) / len(similarities) if similarities else 1

    def _string_similarity(self, s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0
        if s1 == s2:
            return 1
        d = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
        for i in range(len(s1) + 1):
            d[i][0] = i
        for j in range(len(s2) + 1):
            d[0][j] = j
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + cost)
        max_len = max(len(s1), len(s2))
        return 1 - d[-1][-1] / max_len

    def _edge_similarity(self, e1: np.ndarray, e2: np.ndarray) -> float:
        if e1.shape != e2.shape:
            return 0
        return 1 - np.mean(np.abs(e1 - e2)) / 255

    def capture_button(self, button_type: str) -> ButtonData:
        print(f"Looking for {button_type} button...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        button_region = self._find_button(screenshot_np)
        if not button_region:
            return None

        print("Press Space to confirm or click actual button location.")
        print("Press Esc to cancel.")

        while True:
            if keyboard.is_pressed('space'):
                click_pos = (button_region[0] + button_region[2] // 2, button_region[1] + button_region[3] // 2)
                break
            elif keyboard.is_pressed('esc'):
                return None
            if pyautogui.mouseDown():
                click_pos = pyautogui.position()
                if not self._is_in_region(click_pos, button_region):
                    button_region = (click_pos[0] - 50, click_pos[1] - 20, 100, 40)
                break
            time.sleep(0.1)

        button_img = screenshot_np[button_region[1]:button_region[1]+button_region[3], button_region[0]:button_region[0]+button_region[2]]
        text = pytesseract.image_to_string(button_img).strip()
        click_offset = (click_pos[0] - button_region[0], click_pos[1] - button_region[1])
        
        return ButtonData(image=self._np_to_base64(button_img), text=text, region=button_region, click_offset=click_offset, timestamp=time.time())

    def run_calibration(self) -> None:
        button_types = ["launcher", "website"]
        for button_type in button_types:
            for i in range(3):
                print(f"\nCalibrating {button_type} button ({i+1}/3)")
                button_data = self.capture_button(button_type)
                if button_data:
                    self.calibration_data[f"{button_type}_{i}"] = button_data
                    print(f"Successfully captured {button_type} button")
                else:
                    print("Calibration cancelled")
                    return
        
        if click.confirm("Save calibration data for future use?"):
            self.save_config()

    @staticmethod
    def _find_button(image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 80 < w < 200 and 30 < h < 60:
                return (x, y, w, h)
        return None

    @staticmethod
    def _is_in_region(pos: Tuple[int, int], region: Tuple[int, int, int, int]) -> bool:
        return (region[0] <= pos[0] <= region[0] + region[2] and 
                region[1] <= pos[1] <= region[1] + region[3])

    @staticmethod
    def _np_to_base64(image: np.ndarray) -> str:
        pil_img = Image.fromarray(image)
        img_byte_arr = io.BytesIO()
        pil_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return f"data:image/png;base64,{base64.b64encode(img_byte_arr).decode()}"

def base64_to_image(base64_str: str) -> Image.Image:
    img_data = base64.b64decode(base64_str.split(',')[1])
    return Image.open(io.BytesIO(img_data))

def find_and_click(image: Image.Image, name: str, threshold: float = 0.9) -> None:
    try:
        location = pyautogui.locateOnScreen(image, confidence=threshold)
        if location:
            pyautogui.click(location.left + 5, location.top + 5)
            print(f"Found and clicked {name}")
            if name == "Website Download":
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'w')
        time.sleep(2)
    except pyautogui.ImageNotFoundException:
        print(f"{name} not found, waiting...")
        time.sleep(3)

@click.command()
@click.option('-c', '--calibrate', is_flag=True, help='Run calibration mode')
@click.option('-l', '--load-config', is_flag=True, help='Load calibrated button data')
def main(calibrate: bool, load_config: bool) -> None:
    pyautogui.FAILSAFE = False
    
    if calibrate:
        calibration = CalibrationManager()
        calibration.run_calibration()
        return
        
    if load_config:
        calibration = CalibrationManager()
        if not calibration.calibration_data:
            print("No calibration data found. Run with --calibrate first.")
            return
        launcher_img = base64_to_image(calibration.calibration_data['launcher_0'].image)
        website_img = base64_to_image(calibration.calibration_data['website_0'].image)
    else:
        launcher_img = base64_to_image(LAUNCHER_IMG)
        website_img = base64_to_image(WEBSITE_IMG)
    
    print("Starting auto-clicker. Press Ctrl+C to exit.")
    while True:
        find_and_click(launcher_img, "Launcher Download")
        find_and_click(website_img, "Website Download")

if __name__ == "__main__":
    main()