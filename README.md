# Fake Mouse

Fake Mouse is a Python utility that automatically moves your mouse cursor randomly within a defined radius on your screen. Useful for keeping your system active or simulating user activity.

## Features
- Moves mouse cursor randomly within a 500px radius from the center of the screen
- Random delay between movements (1-3 seconds)
- Double-click anywhere to stop the program
- Console output shows movement and elapsed time

## Requirements
- Python 3.x
- `pyautogui` and `pynput` libraries

## Installation
1. Clone this repository or download the source code.
2. Install dependencies:
	```bash
	pip install pyautogui pynput
	```

## Usage
Run the script:
```bash
python main.py
```
Or build a standalone executable (Windows):
```bat
build.bat
```
The program will start after a 3-second delay. Double-click your mouse to exit.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
