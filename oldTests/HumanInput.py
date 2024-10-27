from pynput import keyboard


class HumanInput:
    def keyPress(key):
        print(key)
    with keyboard.Listener(on_press=keyPress) as listener: listener.join()


