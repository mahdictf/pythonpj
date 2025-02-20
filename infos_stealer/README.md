# Ultimate Info Stealer Simulation

## Overview

This repository contains a sophisticated simulation of an info stealer designed for educational purposes. It demonstrates various techniques used in real-world malware, including keylogging, clipboard monitoring, file stealing, screenshot capturing, and encrypted communication. The setup process is automated to make it easy to run and demonstrate these features.

## Features

- **Keylogging**: Captures keystrokes and sends them to a remote server.
- **Clipboard Monitoring**: Monitors and logs clipboard content.
- **File Stealing**: Steals files from specified directories.
- **Screenshot Capturing**: Captures screenshots of the desktop.
- **Encrypted Communication**: Encrypts data before sending it to the remote server.
- **Persistent Installation**: Ensures the script runs at startup.
- **Comprehensive System Information**: Collects detailed system information.
- **Automated Setup**: Installs all prerequisites and configures Ngrok automatically.

## Prerequisites

- **Python**: Ensure you have Python installed on your system. You can download it from [Python's official website](https://www.python.org/).

## Setup Instructions

1. Clone the Repository:

   ```sh
   git clone https://github.com/yourusername/ultimate-info-stealer-simulation.git
   cd ultimate-info-stealer-simulation
   ```

2. **Run the Full Setup Script**:

   - Open a terminal or command prompt.
   - Navigate to the directory containing the scripts.
   - Run the full setup script:
     ```sh
     python setup_full.py
     ```

3. **Follow Prompts**:

   - The script will install all required Python packages.
   - It will download and configure Ngrok.
   - It will create a `config.json` file with default settings.
   - It will generate an encryption key and prompt you to update the `config.json` file with your Ngrok token and the generated encryption key.

4. **Update Configuration File**:

   - Open `config.json` and update the `ngrok_token` and `encryption_key` fields with your Ngrok token and the generated encryption key.

5. **Run the Setup Script Again**:

   - Run the setup script again to start Ngrok and the main script:
     ```sh
     python setup_full.py
     ```

6. **Monitor the Output**:
   - The setup script will start Ngrok and run the main script.
   - The main script will hide itself, collect system information, simulate keylogging, monitor clipboard, steal files, capture screenshots, and send encrypted data to the remote server.

## Important Considerations

- **Ethical Use**: Ensure you have explicit permission to run this script and that it does not interfere with any real systems.
- **Legal Compliance**: Always ensure that your activities comply with local laws and regulations.
- **Educational Value**: Use this script to teach about data handling, network communication, and ethical considerations in cybersecurity.

## Disclaimer

This simulation is intended for educational purposes only. Unauthorized use of this script is illegal and unethical. Use it responsibly and with proper authorization.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
