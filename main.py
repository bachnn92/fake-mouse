import time
import random
import math
import pyautogui
from pynput import mouse

def get_screen_center():
    screen_width, screen_height = pyautogui.size()
    return screen_width // 2, screen_height // 2

def move_mouse_to_center(center_x, center_y):
    pyautogui.moveTo(center_x, center_y, duration=1)

def random_point_in_circle(center_x, center_y, radius):
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(0, radius)
    x = int(center_x + r * math.cos(angle))
    y = int(center_y + r * math.sin(angle))
    return x, y

def get_elapsed(start_time):
    return time.time() - start_time

class DoubleClickDetector:
    def __init__(self, threshold=0.3):
        self.last_click_time = 0
        self.double_click_detected = False
        self.threshold = threshold

    def on_click(self, x, y, button, pressed):
        if pressed:
            current_time = time.time()
            if current_time - self.last_click_time < self.threshold:
                self.double_click_detected = True
            self.last_click_time = current_time

def automove_mouse(radius=500, delay_range=(1, 3)):
    print("Automove after 3 seconds. Double click to exit.")
    start_time = time.time()
    center_x, center_y = get_screen_center()
    move_mouse_to_center(center_x, center_y)
    time.sleep(3)

    detector = DoubleClickDetector()
    listener = mouse.Listener(on_click=detector.on_click)
    listener.start()

    try:
        while True:
            if detector.double_click_detected:
                print("Double click detected. Exiting...")
                time.sleep(3)
                break
            x, y = random_point_in_circle(center_x, center_y, radius)
            delay = random.uniform(*delay_range)
            elapsed = get_elapsed(start_time)
            print(f"Move to ({x}, {y}), delay: {delay:.2f} seconds, Elapsed: {elapsed:.2f} seconds")
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(delay)
    finally:
        listener.stop()

if __name__ == "__main__":
    automove_mouse()
