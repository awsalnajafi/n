import subprocess
import threading
import time

start_port = 5555
end_port = 5755

reservation_x = 200
reservation_y = 1900

yes_x = 313
yes_y = 1239

amount_x = 333
amount_y = 554

coordinates = {
    'online_booking_procedure': [920, 922],
    'Traveler': [330, 339],
    'City': [330, 339],
    'Baghdad': [330, 339],
    'Branch': [330, 339],
    'Jamila': [330, 339],
    'Next': [330, 339],
    'Date_of_travel': [330, 339],
    'May_12': [330, 339],
    'Airports': [330, 339],
    'baghdad': [330, 339],
    'destination': [330, 339],
    'Afghanistan': [330, 339]
}
coordinates_input = {
    'First_Name': [330, 339],
    'Father_Name': [330, 339],
    'GrandFather_Name': [330, 339]
}


def connect_to_port(port):
    try:
        # Attempt to connect to the specified port silently
        subprocess.run(["adb", "connect", f"127.0.0.1:{port}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        pass  # Ignore any exceptions that occur


def control_device(device_id):
    subprocess.run(["adb", "-s", device_id, "shell", "am", "start", "-n",
                    "com.oswatech.rayyan.app/com.example.flutter_application_2.MainActivity"])
    time.sleep(20)

    # Loop through the dictionary and access each item
    for element, (x, y) in coordinates.items():
        subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)])
        time.sleep(5)

    for element, (x, y) in coordinates_input.items():
        subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)])
        time.sleep(1)
        subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_PASTE"])
        time.sleep(1)

    subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(amount_x), str(amount_y)])
    time.sleep(1)
    subprocess.run(["adb", "-s", device_id, "shell", "input", "text", "3000"])

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
    for port in range(start_port, end_port + 1):
        connect_to_port(port)

    # List all connected devices without printing the output
    subprocess.run(["adb", "devices"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
