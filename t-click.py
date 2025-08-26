import json
import time
import pyautogui
import tkinter as tk
import threading
import argparse
from pynput import keyboard   # global key listener

ZONE_FILE = "zone.json"

# Config
STEP = 50         # pixels between clicks vertically
CLICK_DELAY = 0.2 # delay between clicks (sec)


class ZoneWorker:
    def __init__(self, visual=False):
        with open(ZONE_FILE, "r") as f:
            data = json.load(f)
        zone = data["zone"]

        self.left = int(min(zone[0], zone[2]))
        self.top = int(min(zone[1], zone[3]))
        self.right = int(max(zone[0], zone[2]))
        self.bottom = int(max(zone[1], zone[3]))

        print(f"Loaded zone: ({self.left}, {self.top}) → ({self.right}, {self.bottom})")

        self.exit_flag = False
        self.visual = visual

        if self.visual:
            self.root = tk.Tk()
            self.root.attributes("-fullscreen", True)
            self.root.attributes("-alpha", 0.3)
            self.root.configure(bg="gray")
            self.root.attributes("-topmost", True)

            self.canvas = tk.Canvas(self.root, bg="gray", highlightthickness=0)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
                                         outline="red", width=2)
            self.root.bind("<Escape>", self.on_escape)
        else:
            self.root = None

        # Start worker thread
        threading.Thread(target=self.worker, daemon=True).start()

        # Start global ESC listener
        listener = keyboard.Listener(on_press=self.on_key)
        listener.daemon = True
        listener.start()

    def on_key(self, key):
        if key == keyboard.Key.esc:  # ESC pressed
            self.on_escape()

    def on_escape(self, event=None):
        if not self.exit_flag:
            print("ESC pressed. Exiting...")
            self.exit_flag = True
            if self.root:
                self.root.destroy()

    def worker(self):
        while not self.exit_flag:
            # From top to bottom
            for y in range(self.top, self.bottom + 1, STEP):
                if self.exit_flag:
                    break
                x = (self.left + self.right) // 2  # middle X
                pyautogui.click(x, y)
                print(f"Clicked at ({x}, {y})")
                time.sleep(CLICK_DELAY)

            if self.exit_flag:
                break

            # At bottom → press right arrow
            pyautogui.press("right")
            print("Pressed Right Arrow")
            time.sleep(0.5)

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
