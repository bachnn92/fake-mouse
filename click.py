import json
import time
import random
import pyautogui
import tkinter as tk
import threading
import argparse
import keyboard  # pip install keyboard

ZONE_FILE = "zone.json"

# Config
CLICK_MIN = 0.1   # min delay between clicks (sec)
CLICK_MAX = 1.0   # max delay between clicks (sec)
KEY_INTERVAL = 5  # press Right Arrow every 5 sec


class ZoneWorker:
    def __init__(self, visual=False):
        # Load zone from JSON
        with open(ZONE_FILE, "r") as f:
            data = json.load(f)
        zone = data["zone"]  # [x1, y1, x2, y2]

        # Normalize zone
        self.left = int(min(zone[0], zone[2]))
        self.top = int(min(zone[1], zone[3]))
        self.right = int(max(zone[0], zone[2]))
        self.bottom = int(max(zone[1], zone[3]))

        print(f"Loaded zone: ({self.left}, {self.top}) → ({self.right}, {self.bottom})")

        self.exit_flag = False
        self.visual = visual

        if self.visual:
            # Tkinter overlay
            self.root = tk.Tk()
            self.root.attributes("-fullscreen", True)
            self.root.attributes("-alpha", 0.3)
            self.root.configure(bg="gray")
            self.root.attributes("-topmost", True)

            self.canvas = tk.Canvas(self.root, bg="gray", highlightthickness=0)
            self.canvas.pack(fill=tk.BOTH, expand=True)

            # Draw zone rectangle
            self.canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
                                         outline="red", width=2)

            self.root.bind("<Escape>", self.on_escape)  # ESC to exit in visual mode
        else:
            self.root = None  # no GUI

        # Global ESC listener (always works)
        keyboard.add_hotkey("esc", self.on_escape)

        # Worker thread
        threading.Thread(target=self.worker, daemon=True).start()

    def on_escape(self, event=None):
        if not self.exit_flag:
            print("ESC pressed. Exiting...")
            self.exit_flag = True
            if self.root:
                self.root.destroy()

    def worker(self):
        last_key_time = time.time()
        while not self.exit_flag:
            # Random click position inside zone
            x = random.randint(self.left, self.right)
            y = random.randint(self.top, self.bottom)
            pyautogui.click(x, y)
            print(f"Clicked at ({x}, {y})")

            # Random delay
            time.sleep(random.uniform(CLICK_MIN, CLICK_MAX))

            # Press right arrow every KEY_INTERVAL sec
            if time.time() - last_key_time >= KEY_INTERVAL:
                pyautogui.press("right")
                print("Pressed Right Arrow")
                last_key_time = time.time()

    def run(self):
        if self.visual and self.root:
            self.root.mainloop()
        else:
            while not self.exit_flag:
                time.sleep(0.2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--visual", action="store_true",
                        help="Show overlay rectangle")
    args = parser.parse_args()

    worker = ZoneWorker(visual=args.visual)
    worker.run()


if __name__ == "__main__":
    main()
