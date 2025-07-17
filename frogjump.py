#============================== Defualt Imports ==============================#
import time
import sys
import os
import ctypes

#============================== Hotkey Setup ==============================#
start_script_key = 'f'
end_script_key = 'esc'

#============================== Clear Terminal On Run ==============================#
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_terminal()

#============================== Import Error Handler ==============================#
try:
    import keyboard
except ImportError:
    print("Missing required package: 'keyboard'")
    print("Install it with: pip install keyboard")
    sys.exit(1)

#============================== Intro Asci Art ==============================#
def intro():
    print('''
   ___                 _                 _   ___                 _   _             
  /___\__   _____ _ __| | ___   __ _  __| | / __\   _ _ __   ___| |_(_) ___  _ __  
 //  //\ \ / / _ \ '__| |/ _ \ / _` |/ _` |/ _\| | | | '_ \ / __| __| |/ _ \| '_ \ 
/ \_//  \ V /  __/ |  | | (_) | (_| | (_| / /  | |_| | | | | (__| |_| | (_) | | | |
\___/    \_/ \___|_|  |_|\___/ \__,_|\__,_\/    \__,_|_| |_|\___|\__|_|\___/|_| |_|
                                      Frog Jump                                            
''')
    print(f"Press '{start_script_key}' to frog jump. Press {end_script_key} to quit.")

#============================== Exit Handler ==============================#
def exit():
    print("Successfully exited script.")
    sys.exit()

#============================== Mouse Movement Setup ==============================#
PUL = ctypes.POINTER(ctypes.c_ulong)

class MouseInput(ctypes.Structure):
    _fields_ = (("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL))

class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def send_mouse_move(dx, dy):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.mi = MouseInput(dx, dy, 0, 0x0001, 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

#============================== Frog Jump Macro ==============================#
def frog_jump():
    time.sleep(1)

    keyboard.press('s')
    time.sleep(0.1)
    keyboard.release('s')

    keyboard.press('space')

    time.sleep(0.1)
    keyboard.press('w')
    time.sleep(0.1)
    keyboard.release('w')

    for _ in range(10):
        send_mouse_move(50, 0)
        time.sleep(0.002)

    time.sleep(0.05)

    for _ in range(15):
        send_mouse_move(-50, 0)
        time.sleep(0.002)

    time.sleep(0.3)

#============================== Hotkey ==============================#
keyboard.add_hotkey(start_script_key, frog_jump)
keyboard.add_hotkey(end_script_key, exit)

#============================== Start ==============================#
intro()
keyboard.wait()