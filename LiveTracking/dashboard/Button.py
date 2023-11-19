import keyboard

# Variable to keep track of space button presses
space_count = 0

# Function to be called whenever the space key is pressed
def on_space_press(event):
    global space_count
    space_count += 1
    print(f"Space key pressed {space_count} times")

# Listen for space key press events
keyboard.on_press_key("space", on_space_press)

# Keep the script running to listen for key presses
print("Press the space key to increase count. Press ESC to stop.")
keyboard.wait('esc')  # Wait for the escape key to stop the script

print(f"Final space key press count: {space_count}")
