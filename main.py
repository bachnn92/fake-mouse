import time
import random
import math
import pyautogui
from pynput import mouse

# Wait for 2 seconds before starting
start_time = time.time()
print("Automove after 3 seconds. Double click to exit.")
time.sleep(3)

# Get screen size and calculate center
screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

# Move mouse to center
pyautogui.moveTo(center_x, center_y, duration=1)

# Fixed radius
radius = 500
delay_range = [1, 3]  # Delay range in seconds

# Variable to track if double-click occurred
double_click_detected = False

# Define the mouse listener callback
def on_click(x, y, button, pressed):
    global last_click_time, double_click_detected
    if pressed:
        current_time = time.time()
        if current_time - last_click_time < 0.3:  # 300ms double-click threshold
            double_click_detected = True
        last_click_time = current_time
# Add timestamp and elapsed time tracking
def get_elapsed():
    elapsed = time.time() - start_time
    return elapsed

# Start mouse listener in the background
last_click_time = 0
listener = mouse.Listener(on_click=on_click)
listener.start()

# Move randomly within the radius
while True:
    if double_click_detected:
        print("Double click detected. Exiting...")
        time.sleep(3)
        break
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(0, radius)
    x = int(center_x + r * math.cos(angle))
    y = int(center_y + r * math.sin(angle))
    delay = random.uniform(delay_range[0], delay_range[1])
    elapsed = get_elapsed()
    print(f"Move to ({x}, {y}), delay: {delay:.2f} seconds, Elapsed: {elapsed:.2f} seconds")
    pyautogui.moveTo(x, y, duration=0.5)
    time.sleep(delay)

listener.stop()
