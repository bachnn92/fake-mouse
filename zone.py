import tkinter as tk
import json
import os

ZONE_FILE = "zone.json"  # permanent JSON file


class ZoneSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)  # semi-transparent
        self.root.configure(bg="gray")
        self.root.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.root, bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.zone = None
        self.dbl_clicked = False

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)

        # ESC to exit
        self.root.bind("<Escape>", self.on_escape)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.rect:
            self.zone = self.canvas.coords(self.rect)
            print(f"Zone selected: {self.zone}")
            self.save_zone()

    def on_double_click(self, event):
        print("Double-click detected. Exiting...")
        self.dbl_clicked = True
        self.root.destroy()

    def on_escape(self, event):
        print("ESC pressed. Exiting...")
        self.root.destroy()

    def save_zone(self):
        """Save the selected zone to a JSON file"""
        if self.zone:
            with open(ZONE_FILE, "w") as f:
                json.dump({"zone": self.zone}, f, indent=4)
            print(f"Zone saved to {ZONE_FILE}")

    def run(self):
        self.root.mainloop()
        return self.zone


def main():
    selector = ZoneSelector()
    zone = selector.run()
    print("Final Zone:", zone)

    # If JSON file exists, show its contents
    if os.path.exists(ZONE_FILE):
        with open(ZONE_FILE, "r") as f:
            print("Saved zone in JSON file:", json.load(f))


if __name__ == "__main__":
    main()
