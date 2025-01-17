# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyautogui",
#     "pillow",
#     "opencv-python",
# ]
# ///

import base64
import io
from typing import Optional
import time
import pyautogui
from PIL import Image

LAUNCHER_IMG = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAZCAYAAABuKkPfAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKpSURBVFhH7VbfaxNBEPav66v/gCD4Jr4ogj8qilDEF6U+9M2KVoVam1q1SpE+RBppTbXFSpqkl2Qvyd0l9zP/wjjfnHdc9VpSvILQffi43ZnZnZlvZ2fvTGN6gk47NAkMTQJDk8DQJDA0CQxNAuNQEty9dRqNRjGikILuHpnvpnJti4T5fopCuy3fPP1x0Xl1hYJek6zybK4eOJIEX/2UcWf+MnnNTQodk9TSrb9si8R/SwLQfnmJgv4+DbZX0rm3X5UqiUKf3Npnaj29QM7mAjttUPvFRTKenOdxnQY7H2VNf21GErTKjyUwt7FBUeDJHm6tTM2ZswdIwNyplijyh1yREVdjPa1G6Ia7a+IbOt+skXp9TXTdD/f5wFS8pm/IuBASUlnnRzoO7Bap0mTqFAR1V+5JEpD1Vh9Q5DmyjyT0bVnGavGG2GAvkGlV5igc9sQ+SwICj1ybrPVnMenNr0xETciFTNZ8eiQxiH8mG+TjENzGFzJmz5FdeR7vUSgJLOssXBUC7I35VIcAcOrqzW0JAjqnuiSJygku35EkYPdniUrinBDmWRLceoW81nbqo7f6kMKBKV8kqxavpzrYIr74QGIbyAu9DqmMk8oGneiQMIKHU9gBnrElZPjtnd/XpC5rxiUB/rFP4iNrJ32q9Z2vUpA2cNhCBxvYYs2J9QSpBMuQUkv0SSWgVCHHXURF4HpAhzuLuSrdPF4lcPUkPrKVgDhQjebbu6JLCDuxSsh7HaDP6wnQofSRFK4BSEFDRHPDycl+Y5KA+WE9AU0RpEOeJI6YpBmzTWE9Ifuf4KvdA/8JElTO6wCdBMIBIlCxRbPiKkJjxHxcEo56HfASIFnIsRaVljTt5FD++XU4TdAkMDQJDE0CQ5PA0CQwNAkMTQJDkzA9Qb8ALwHi52gP8aUAAAAASUVORK5CYII="
WEBSITE_IMG = "data:image/jpeg;base64,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"

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

def main() -> None:
    pyautogui.FAILSAFE = False
    launcher_img = base64_to_image(LAUNCHER_IMG)
    website_img = base64_to_image(WEBSITE_IMG)
    
    while True:
        find_and_click(launcher_img, "Launcher Download")
        find_and_click(website_img, "Website Download")

if __name__ == "__main__":
    main()