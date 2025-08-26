
import subprocess
import sys

if __name__ == "__main__":
    # Step 1: Run zone.py to select and save the zone
    print("Select a zone (draw rectangle, double-click or press ESC to finish)...")
    result = subprocess.run([sys.executable, "zone.py"])
    if result.returncode != 0:
        print("Zone selection cancelled or failed.")
        sys.exit(1)

    # Step 2: Run click.py to start clicking in the selected zone
    print("Starting auto-clicker in selected zone...")
    subprocess.run([sys.executable, "click.py"])
