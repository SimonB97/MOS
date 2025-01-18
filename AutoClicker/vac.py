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

@dataclass
class ButtonMatch:
    region: Tuple[int, int, int, int]
    confidence: float
    screenshot: np.ndarray

class CalibrationManager:
    def __init__(self, config_path: str = "button_calibration.json"):
        self.config_path = config_path
        self.calibration_data: Dict[str, ButtonData] = {}
        self.thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]
        self.max_attempts = 3
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

    def capture_button(self, button_type: str) -> Optional[ButtonData]:
        print(f"\nLooking for {button_type} button...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        
        matches = self._find_button_candidates(screenshot_np)
        if not matches:
            print("No button candidates found. Try adjusting lighting or window position.")
            return None

        selected_match = self._select_button_match(matches)
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
        text = pytesseract.image_to_string(button_img).strip()
        click_offset = (click_pos[0] - button_region[0], click_pos[1] - button_region[1])
        
        return ButtonData(
            image=self._np_to_base64(button_img),
            text=text,
            region=button_region,
            click_offset=click_offset,
            timestamp=time.time()
        )

    def _find_button_candidates(self, screenshot: np.ndarray) -> List[ButtonMatch]:
        matches = []
        
        # Convert screenshot to grayscale once
        gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        
        for threshold in self.thresholds:
            try:
                # Apply adaptive thresholding
                binary = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )
                
                # Find contours
                contours, _ = cv2.findContours(
                    binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                
                # Filter contours by size and shape
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    if 80 < w < 200 and 30 < h < 60:
                        # Calculate match confidence based on shape and size
                        aspect_ratio = w / h
                        size_score = min(w * h, 8000) / 8000
                        confidence = (aspect_ratio * 0.4 + size_score * 0.6) * threshold
                        
                        if confidence >= threshold:
                            # Check if we already found this region with higher confidence
                            is_duplicate = False
                            for match in matches:
                                if self._regions_overlap(match.region, (x, y, w, h)):
                                    is_duplicate = True
                                    break
                            if not is_duplicate:
                                matches.append(ButtonMatch(
                                    region=(x, y, w, h),
                                    confidence=confidence,
                                    screenshot=screenshot
                                ))
                
            except Exception as e:
                print(f"Error during detection: {e}")
                continue

        return sorted(matches, key=lambda x: x.confidence, reverse=True)

    def _regions_overlap(self, r1: Tuple[int, int, int, int], r2: Tuple[int, int, int, int]) -> bool:
        """Check if two regions (x, y, w, h) overlap"""
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    def _select_button_match(self, matches: List[ButtonMatch]) -> Optional[ButtonMatch]:
        if not matches:
            return None
            
        # Create a copy of the screenshot to draw on
        preview = matches[0].screenshot.copy()
        
        # Draw all candidates with numbers
        for i, match in enumerate(matches):
            x, y, w, h = match.region
            # Draw rectangle
            cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Draw number with background
            label = f"{i + 1}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            (label_w, label_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
            
            # Draw white background for number
            cv2.rectangle(preview, 
                         (x, y - label_h - 10), 
                         (x + label_w + 10, y), 
                         (255, 255, 255), 
                         -1)
            # Draw number
            cv2.putText(preview, 
                        label,
                        (x + 5, y - 5),
                        font,
                        font_scale,
                        (0, 0, 0),
                        thickness)
        
        # Show preview window
        window_name = "Button Candidates"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, preview)
        cv2.waitKey(100)  # Give time for window to render
        
        # Print candidates info
        print("\nButton candidates found:")
        for i, match in enumerate(matches):
            print(f"{i + 1}: Confidence {match.confidence:.2f}")
        
        while True:
            try:
                choice = input("\nEnter number of correct button (or 0 to cancel): ")
                if choice == "0":
                    cv2.destroyWindow(window_name)
                    cv2.waitKey(1)  # Process window destruction
                    return None
                index = int(choice) - 1
                if 0 <= index < len(matches):
                    cv2.destroyWindow(window_name)
                    cv2.waitKey(1)  # Process window destruction
                    return matches[index]
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except cv2.error:
                print("Window closed. Cancelling selection.")
                return None

    def _show_candidate(self, match: ButtonMatch, title: str) -> None:
        """Helper method to show a single candidate"""
        region = match.region
        button_img = match.screenshot[
            region[1]:region[1]+region[3], 
            region[0]:region[0]+region[2]
        ]
        cv2.imshow(title, button_img)
        cv2.waitKey(1)  # Show window without blocking
        time.sleep(1)  # Give time to see the preview
        cv2.destroyAllWindows()

    def _get_click_position(self, region: Tuple[int, int, int, int]) -> Optional[Tuple[int, int]]:
        print("\nPress Space to confirm center position or click desired location.")
        print("Press Esc to cancel.")
        
        while True:
            if keyboard.is_pressed('space'):
                return (region[0] + region[2] // 2, region[1] + region[3] // 2)
            elif keyboard.is_pressed('esc'):
                return None
            elif pyautogui.mouseDown():
                pos = pyautogui.position()
                if self._is_in_region(pos, region):
                    return pos
                print("Click must be within the button region.")
            time.sleep(0.1)

    def run_calibration(self, button_type: str) -> None:
        print(f"\nCalibrating {button_type} button")
        for i in range(3):
            print(f"\nCapture {i+1}/3")
            button_data = self.capture_button(button_type)
            if button_data:
                self.calibration_data[f"{button_type}_{i}"] = button_data
                print(f"Successfully captured {button_type} button")
        
        save_choice = click.confirm("Save calibration data for future use?")
        if save_choice:
            self.save_config()
            
        # Start auto-clicking after calibration
        button_img = base64_to_image(self.calibration_data[f"{button_type}_0"].image)
        print("Starting auto-clicker. Press Ctrl+C to exit.")
        while True:
            find_and_click(button_img, f"{button_type} Download")

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
@click.option('-c', '--calibrate', type=click.Choice(['web', 'launcher']), help='Run calibration mode for specific button')
@click.option('-l', '--load-config', is_flag=True, help='Load calibrated button data')
def main(calibrate: str, load_config: bool) -> None:
    pyautogui.FAILSAFE = False
    
    if calibrate:
        button_type = "website" if calibrate == "web" else "launcher"
        calibration = CalibrationManager()
        calibration.run_calibration(button_type)
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
