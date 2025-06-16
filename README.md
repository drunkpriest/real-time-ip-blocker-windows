# Dynamic Firewall Rule Generator

A Python-based GUI tool to dynamically manage Windows Firewall rules.  
This tool allows users to block or unblock specific IP addresses for inbound, outbound, or both traffic directions. Useful for network access control, cybersecurity labs, system administration, and educational purposes.

## 🔧 Features

- Block IP addresses using Windows Firewall
- Unblock IP addresses with dropdown selection
- Inbound / Outbound / Both direction blocking supported
- Automatic DNS flush after unblocking
- Real-time command log window
- GUI built with Python `tkinter`
- JSON-based rule storage for easy management
- Requires Administrator privileges to modify firewall rules

## 💻 Technologies Used

- Python 3.x
- tkinter (GUI)
- subprocess module (system command execution)
- netsh (Windows Firewall command-line tool)
- ipconfig (DNS flushing)

## ⚠ Requirements

- Windows OS
- Python 3 installed
- Run the script as Administrator

## 📂 Files Included

- `firewall_rule_manager.py` → Main source code
- `windows_firewall_rules.json` → Rule storage file

## 🚀 Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/dynamic-firewall-rule-generator.git
    ```
2. Navigate to the project folder:
    ```bash
    cd dynamic-firewall-rule-generator
    ```
3. Run the script as Administrator:
    ```bash
    python firewall_rule_manager.py
    ```

> ⚠ Note: Always run this tool with Admin privileges or you'll get permission errors.


## 📌 Disclaimer

This tool is intended for educational and research purposes only.

- Always use with caution on your personal system.
- Do not use this tool in any production, enterprise, or unauthorized network environment.
- Modifying firewall rules may disrupt network connectivity or other applications.
- The author is not responsible for any damage, data loss, or network outages caused by improper usage of this tool.
- Use only on systems where you have full permission to modify firewall settings.
