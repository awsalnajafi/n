#!/bin/bash

# Set device ID as a variable
device_id="127.0.0.1:6555"

# Updated coordinates for the "Reservation" button
reservation_x=200
reservation_y=1900

# Coordinates for the "Yes" button (assuming these remain the same unless specified otherwise)
yes_x=313
yes_y=1239

# Loop indefinitely
while true; do
    # Click the "Reservation" button twice with a 2-second delay between clicks
    adb -s $device_id shell input tap $reservation_x $reservation_y

    sleep 1
    adb -s $device_id shell input tap $reservation_x $reservation_y

    # Wait for 5 seconds after the second click
    sleep 1

    # Click the "Yes" button
    adb -s $device_id shell input tap $yes_x $yes_y

    # Delay before starting the next iteration, if necessary
    sleep 1  # Adjust this value if needed to control loop frequency
done

