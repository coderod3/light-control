import http.client

from pynput import keyboard, mouse

# ESP8266 IP address and pin control paths
ESP8266_IP = "192.168.0.116"

# Global variables to store the state of each pin
lamp_state = False
led_state = False
tomada_state = False


def send_request(pin, state):
    # print('request sent.', state)
    """
    Send an HTTP request to control the given pin on the ESP8266.
    :param pin: 'D1', 'D2'...
    :param state: 'on' or 'off'
    """
    try:
        # Open connection to ESP8266
        conn = http.client.HTTPConnection(ESP8266_IP, timeout=0.5)

        # Construct the path to control pin
        path = f"/{pin}/{state}"

        # Send the GET request
        conn.request("GET", path)

    except Exception as e:
        print(f"Error sending request: {e}")
    finally:
        # Close connection
        conn.close()


def toggle_lamp():
    """
    Toggles the D1 pin between 'on' and 'off'.
    """
    global lamp_state
    lamp_state = not lamp_state  # Toggle the state
    state = 'on' if lamp_state else 'off'
    send_request('lampada', state)


def toggle_led():
    """
    Toggles the D2 pin between 'on' and 'off'.
    """
    global led_state
    led_state = not led_state  # Toggle the state
    state = 'on' if led_state else 'off'
    send_request('led', state)


def toggle_tomada():
    """
    Toggles the D6 pin between 'on' and 'off'.
    """
    global tomada_state
    tomada_state = not tomada_state  # Toggle the state
    state = 'on' if tomada_state else 'off'
    send_request('tomada', state)


def on_mouse_click(x, y, button, pressed):
    """
    Handles mouse click events for X1 and X2 buttons to control D3 and D8.
    """
    if pressed:
        if button == mouse.Button.x1:
            toggle_lamp()
            # print("X1 mouse button clicked - Toggling D2")
        elif button == mouse.Button.x2:
            toggle_led()
            # print("X2 mouse button clicked - Toggling D1")
        #elif button == mouse.Button.middle:
        #   toggle_tomada()


if __name__ == "__main__":

    # Set up mouse listener for X1 and X2 buttons
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    mouse_listener.start()

    # Define the hotkeys
    hotkeys = keyboard.GlobalHotKeys({
        '<alt_gr>+,': toggle_lamp,
        '<alt_gr>+.': toggle_led,
        '<alt_gr>+;': toggle_tomada
    })

    try:
        # Start listening for keyboard shortcuts
        hotkeys.start()
        hotkeys.join()
    except Exception as e:
        print(f"Error in keyboard listener: {e}")
