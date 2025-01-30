import http.client
from pynput import keyboard, mouse

ESP8266_IP = "192.168.0.116"
TIMEOUT = 2

# Global states
lamp_state = False
led_state = False
tomada_state = False


def send_request(pin, state):
    """Send HTTP request and return True if successful"""
    try:
        conn = http.client.HTTPConnection(ESP8266_IP, timeout=TIMEOUT)
        path = f"/{pin}/{state}"
        conn.request("GET", path)
        response = conn.getresponse()
        return response.status == 200
    except:
        return False
    finally:
        try:
            conn.close()
        except:
            pass


def toggle_device(device_name, current_state):
    """Generic toggle function with state validation"""
    new_state = not current_state
    state_str = 'on' if new_state else 'off'

    # Retry up to 3 times on failure
    for _ in range(3):
        if send_request(device_name, state_str):
            return new_state
    return current_state  # Return original state if all retries fail


def toggle_lamp():
    global lamp_state
    lamp_state = toggle_device('lampada', lamp_state)


def toggle_led():
    global led_state
    led_state = toggle_device('led', led_state)


def toggle_tomada():
    global tomada_state
    tomada_state = toggle_device('tomada', tomada_state)


def on_mouse_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.x1:
            toggle_lamp()
        elif button == mouse.Button.x2:
            toggle_led()


if __name__ == "__main__":
    # Mouse listener
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    mouse_listener.start()

    # Keyboard hotkeys
    hotkeys = keyboard.GlobalHotKeys({
        '<alt_gr>+,': toggle_lamp,
        '<alt_gr>+.': toggle_led,
        '<alt_gr>+;': toggle_tomada
    })

    try:
        hotkeys.start()
        hotkeys.join()
    finally:
        pass