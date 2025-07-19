import tkinter as tk
import webbrowser
import threading
import time
import sys
import ctypes

#====================== Globals ======================#
start_script_key = 'f'
hotkey_ref = None
timing = 0.1
running = False
setting_hotkey = False

try:
    import keyboard
except ImportError:
    print("Missing required package: 'keyboard'")
    print("Install it with: pip install keyboard")
    sys.exit(1)

#====================== Mouse Input Setup ======================#
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

#====================== Macro Logic ======================#
def frog_jump():
    global running, timing
    time.sleep(1)
    if not running: return
    keyboard.press('s')
    time.sleep(timing)
    keyboard.release('s')
    if not running: return
    keyboard.press('space')
    time.sleep(0.1)
    keyboard.press('w')
    time.sleep(timing)
    keyboard.release('w')
    for _ in range(10):
        if not running: return
        send_mouse_move(50, 0)
        time.sleep(0.002)
    time.sleep(0.05)
    for _ in range(15):
        if not running: return
        send_mouse_move(-50, 0)
        time.sleep(0.002)
    time.sleep(0.3)
    if running:
        threading.Thread(target=frog_jump, daemon=True).start()

#====================== Control Logic ======================#
def toggle_frog_jump():
    global running
    if running:
        running = False
        status_var.set("Paused")
        status_label.config(fg="#FF5555")
    else:
        running = True
        status_var.set("Running")
        status_label.config(fg="#55FF55")
        threading.Thread(target=frog_jump, daemon=True).start()

def update_timing_slider(val):
    global timing
    timing = float(val)
    timing_entry_var.set(f"{timing:.2f}")

def update_timing_entry(event=None):
    global timing
    try:
        val = float(timing_entry_var.get())
        if 0.05 <= val <= 0.5:
            timing = val
            timing_slider.set(val)
        else:
            raise ValueError
    except ValueError:
        timing_entry_var.set(f"{timing:.2f}")

def exit_app():
    global running
    running = False
    root.destroy()
    sys.exit()

def open_github():
    webbrowser.open("https://github.com/OverloadFunction")

#====================== Hotkey Handling ======================#
def apply_new_hotkey(key):
    global start_script_key, hotkey_ref
    try:
        if hotkey_ref:
            keyboard.remove_hotkey(hotkey_ref)
    except Exception:
        pass
    start_script_key = key
    hotkey_status.config(text=f"Hotkey set to: {start_script_key.upper()}", fg="#90EE90")
    try:
        hotkey_ref = keyboard.add_hotkey(start_script_key, toggle_frog_jump)
    except Exception:
        hotkey_status.config(text="Failed to set hotkey.", fg="#FF5555")

def wait_for_hotkey():
    global setting_hotkey
    setting_hotkey = True
    hotkey_status.config(text="Press a key...", fg="#FFD700")  # gold/yellow

    def on_key(e):
        global setting_hotkey
        if not setting_hotkey: return
        key = e.name.lower()
        allowed_keys = [f'f{i}' for i in range(1, 13)] + ['esc', 'space', 'tab']
        if (len(key) != 1 and key not in allowed_keys) or key == 'shift':
            hotkey_status.config(text="Invalid key. Try again...", fg="#FF5555")
            return
        setting_hotkey = False
        keyboard.unhook_all()
        root.after(10, lambda: apply_new_hotkey(key))

    keyboard.hook(on_key)

#====================== GUI Setup ======================#
root = tk.Tk()
root.title("🐸 Frog Jump Macro")
root.geometry("380x300")
root.resizable(False, False)
root.configure(bg="#121212")

font_title = ("Segoe UI", 18, "bold")
font_subtitle = ("Segoe UI", 12)
font_button = ("Segoe UI", 11)
font_small = ("Segoe UI", 10)

title = tk.Label(root, text="🐸 Frog Jump Macro", font=font_title, bg="#121212", fg="#7CFC00")
title.pack(pady=(15, 5))

status_var = tk.StringVar(value="Paused")
status_label = tk.Label(root, textvariable=status_var, font=font_subtitle, fg="#FF5555", bg="#121212")
status_label.pack(pady=(0, 15))

start_button = tk.Button(root, text="Start / Stop (Hotkey)", command=toggle_frog_jump,
                         width=30, bg="#2E8B57", fg="white", font=font_button, activebackground="#3CB371")
start_button.pack(pady=(0, 12))

hotkey_btn = tk.Button(root, text="Set Custom Hotkey", command=wait_for_hotkey,
                       width=30, bg="#444444", fg="white", font=font_button, activebackground="#666666")
hotkey_btn.pack()

hotkey_status = tk.Label(root, text=f"Hotkey set to: {start_script_key.upper()}",
                         bg="#121212", fg="#AAAAAA", font=font_small)
hotkey_status.pack(pady=(5, 15))

# ======= Timing Section =======
timing_frame = tk.Frame(root, bg="#121212")
timing_frame.pack(pady=(0, 20), fill="x", padx=25)

timing_label = tk.Label(timing_frame, text="Timing (seconds):", fg="white", bg="#121212", font=font_subtitle)
timing_label.grid(row=0, column=0, sticky="w")

timing_entry_var = tk.StringVar(value=f"{timing:.2f}")
timing_entry = tk.Entry(timing_frame, width=6, font=font_small, justify="center",
                        textvariable=timing_entry_var, bg="#1E1E1E", fg="white", insertbackground="white",
                        relief="flat", highlightthickness=1, highlightcolor="#7CFC00", highlightbackground="#555555")
timing_entry.grid(row=0, column=1, sticky="w", padx=(10, 0))
timing_entry.bind("<Return>", update_timing_entry)

timing_slider = tk.Scale(timing_frame, from_=0.05, to=0.5, resolution=0.01,
                         orient="horizontal", length=265, command=update_timing_slider,
                         bg="#121212", fg="white", troughcolor="#2E8B57",
                         activebackground="#7CFC00",
                         highlightthickness=0)
timing_slider.set(timing)
timing_slider.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky="w")

timing_frame.grid_columnconfigure(0, weight=0)
timing_frame.grid_columnconfigure(1, weight=0)

# ======= GitHub Button with nicer style =======
def on_enter(e):
    github_button['bg'] = '#2a62b9'

def on_leave(e):
    github_button['bg'] = '#0D47A1'

github_button = tk.Button(root, text="🐙 GitHub: OverloadFunction", command=open_github,
                          bg="#0D47A1", fg="white", font=font_button, activebackground="#1565C0", width=30,
                          relief="flat", borderwidth=0, pady=6)
github_button.pack(pady=(0, 10))
github_button.bind("<Enter>", on_enter)
github_button.bind("<Leave>", on_leave)

exit_button = tk.Button(root, text="Exit", command=exit_app,
                        bg="#B22222", fg="white", font=font_button, activebackground="#CD5C5C", width=30)
exit_button.pack()

#====================== Set Initial Hotkey ======================#
hotkey_ref = keyboard.add_hotkey(start_script_key, toggle_frog_jump)

#====================== Launch GUI ======================#
root.mainloop()