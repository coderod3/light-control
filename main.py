import http.client
from pynput import keyboard, mouse

# ESP8266 IP address and pin control paths
ESP8266_IP = "192.168.0.116"

# Global variables to store the state of each pin
d3_state = False
d8_state = False


def send_request(pin, state):
    """
    Send an HTTP request to control the given pin on the ESP8266.
    :param pin: 'D3' or 'D8'
    :param state: 'on' or 'off'
    """
    try:
        # Open connection to ESP8266
        conn = http.client.HTTPConnection(ESP8266_IP)

        # Construct the path to control pin
        path = f"/{pin}/{state}"

        # Send the GET request
        conn.request("GET", path)
        response = conn.getresponse()

        # Close connection
        conn.close()
        """
        if response.status == 200:
            print(f"Successfully set {pin} to {state}")
        else:
            print(f"Failed to control {pin}, Status code: {response.status}")
        """
    except Exception as e:
        print(f"Error sending request: {e}")


def toggle_d3():
    """
    Toggles the D3 pin between 'on' and 'off'.
    """
    global d3_state
    d3_state = not d3_state  # Toggle the state
    state = 'on' if d3_state else 'off'
    send_request('D3', state)


def toggle_d8():
    """
    Toggles the D8 pin between 'on' and 'off'.
    """
    global d8_state
    d8_state = not d8_state  # Toggle the state
    state = 'on' if d8_state else 'off'
    send_request('D8', state)


def on_mouse_click(x, y, button, pressed):
    """
    Handles mouse click events for X1 and X2 buttons to control D3 and D8.
    """
    if pressed:
        if button == mouse.Button.x1:
            toggle_d8()
            # print("X1 mouse button clicked - Toggling D8")
        elif button == mouse.Button.x2:
            toggle_d3()
            # print("X2 mouse button clicked - Toggling D3")


if __name__ == "__main__":

    # Set up mouse listener for X1 and X2 buttons
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    mouse_listener.start()

    # Define the hotkeys
    hotkeys = {
        '<ctrl>+<shift>+d': toggle_d3,
        '<ctrl>+<shift>+o': toggle_d8
    }

    # Start the listener for the defined hotkeys
    with keyboard.GlobalHotKeys(hotkeys) as h:
        h.join()

    with mouse.Listener(on_click=on_mouse_click) as listener:
        listener.join()
