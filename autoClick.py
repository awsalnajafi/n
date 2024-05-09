import subprocess
import threading
import time

def control_device(device_id):
    # Updated coordinates for the "Reservation" button
    reservation_x = 200
    reservation_y = 1900

    # Coordinates for the "Yes" button
    yes_x = 313
    yes_y = 1239

    # Loop indefinitely
    while True:
        # Click the "Reservation" button twice with a 1-second delay between clicks
        subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(reservation_x), str(reservation_y)])
        time.sleep(1)
        subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(reservation_x), str(reservation_y)])

        # Wait for 1 second after the second click
        time.sleep(1)

        # Click the "Yes" button
        subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(yes_x), str(yes_y)])

        # Delay before starting the next iteration
        time.sleep(1)  # Adjust this value if needed to control loop frequency

def main():
    # Get list of devices
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices = result.stdout.splitlines()

    # Create a thread for each running emulator
    threads = []
    for device in devices[1:]:
        if "device" in device:
            device_id = device.split("\t")[0]
            thread = threading.Thread(target=control_device, args=(device_id,))
            thread.start()
            threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
