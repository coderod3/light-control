# this has a half implemented queue useful for handling the requests and leaving it always at the state that you want
# still missing the esp part that responds with the actual state of the pin currently via a route in the API
# with that in place we can simply tell this program to try the request until the value of the pin in the API changes

import http.client
import threading
import queue
from pynput import keyboard, mouse

# ESP8266 IP address and pin control paths
ESP8266_IP = "192.168.0.116"

# Global variables to store the state of each pin
lamp_state = False
led_state = False
tomada_state = False

# Queue to handle requests
request_queue = queue.Queue()


def send_request(pin, state):
    """
    Send an HTTP request to control the given pin on the ESP8266.
    :param pin: 'lampada', 'led', 'tomada', etc.
    :param state: 'on' or 'off'
    """
    try:
        # Open connection to ESP8266
        conn = http.client.HTTPConnection(ESP8266_IP, timeout=1)

        # Construct the path to control pin
        path = f"/{pin}/{state}"

        # Send the GET request
        conn.request("GET", path)
        response = conn.getresponse()
        print(f"Request sent to {pin}, state: {state}, Response: {response.status}")

    except Exception as e:
        print(f"Error sending request: {e}")
    finally:
        # Close connection
        conn.close()


def process_requests():
    """
    Continuously process requests from the queue.
    """

    while True:
        pin, state = request_queue.get()  # Get the next request from the queue
        send_request(pin, state)
        request_queue.task_done()  # Mark the task as done


def toggle_lamp():
    """
    Toggles the D1 pin between 'on' and 'off'.
    """
    global lamp_state
    lamp_state = not lamp_state  # Toggle the state
    state = 'on' if lamp_state else 'off'
    request_queue.put(('lampada', state))


def toggle_led():
    """
    Toggles the D2 pin between 'on' and 'off'.
    """
    global led_state
    led_state = not led_state  # Toggle the state
    state = 'on' if led_state else 'off'
    request_queue.put(('led', state))


def toggle_tomada():
    """
    Toggles the D6 pin between 'on' and 'off'.
    """
    global tomada_state
    tomada_state = not tomada_state  # Toggle the state
    state = 'on' if tomada_state else 'off'
    request_queue.put(('tomada', state))


def on_mouse_click(x, y, button, pressed):
    """
    Handles mouse click events for X1 and X2 buttons to control D3 and D8.
    """
    if pressed:
        if button == mouse.Button.x1:
            toggle_lamp()
        elif button == mouse.Button.x2:
            toggle_led()


if __name__ == "__main__":

    # Start the request processing thread
    threading.Thread(target=process_requests, daemon=True).start()

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
