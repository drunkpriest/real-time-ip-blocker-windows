import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import json
import re
import os
import subprocess
import socket

RULE_FILE = 'windows_firewall_rules.json'

# Initialize rule file if not exists
if not os.path.exists(RULE_FILE):
    with open(RULE_FILE, 'w') as f:
        json.dump({"blocked_ips": []}, f)

def load_rules():
    with open(RULE_FILE, 'r') as f:
        return json.load(f)

def save_rules(rules):
    with open(RULE_FILE, 'w') as f:
        json.dump(rules, f, indent=4)

def is_valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip)

def resolve_domain(domain):
    try:
        return socket.gethostbyname_ex(domain)[2]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to resolve domain: {e}")
        return []

def block_ip():
    input_value = ip_entry.get().strip()
    direction = block_type_var.get()

    if direction == "":
        messagebox.showerror("Error", "Please select blocking direction.")
        return

    ips_to_block = []

    if is_valid_ip(input_value):
        ips_to_block = [input_value]
    else:
        ips_to_block = resolve_domain(input_value)
        if not ips_to_block:
            return

    rules = load_rules()

    for ip in ips_to_block:
        already_blocked = any(rule['ip'] == ip for rule in rules['blocked_ips'])
        if already_blocked:
            log_text.insert(tk.END, f"{ip} is already blocked.\n")
            continue

        try:
            rule_name = f"Block_{ip}_{direction}"

            if direction in ["IN", "BOTH"]:
                subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name={rule_name}_IN",
                                "dir=in", "action=block", f"remoteip={ip}"], check=True)

            if direction in ["OUT", "BOTH"]:
                subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name={rule_name}_OUT",
                                "dir=out", "action=block", f"remoteip={ip}"], check=True)

            rules['blocked_ips'].append({"ip": ip, "direction": direction})
            save_rules(rules)
            update_dropdown()

            log_text.insert(tk.END, f"Blocked {ip} ({direction})\n")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to execute netsh. Run Python as Administrator.")

    ip_entry.delete(0, tk.END)
    block_type_var.set("")

def unblock_ip():
    selected = unblock_combo.get()
    if not selected:
        messagebox.showwarning("Warning", "Please select IP to unblock.")
        return

    ip, direction = selected.split(" (")
    ip = ip.strip()
    direction = direction.replace(")", "").strip()

    rules = load_rules()

    try:
        rule_name = f"Block_{ip}_{direction}"

        if direction in ["IN", "BOTH"]:
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}_IN"], check=False)

        if direction in ["OUT", "BOTH"]:
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}_OUT"], check=False)

        rules['blocked_ips'] = [rule for rule in rules['blocked_ips'] if rule['ip'] != ip]
        save_rules(rules)
        update_dropdown()

        subprocess.run(["ipconfig", "/flushdns"], check=False)
        subprocess.run(["netsh", "interface", "ip", "delete", "arpcache"], check=False)

        log_text.insert(tk.END, f"Unblocked {ip} ({direction})\n")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to execute netsh.")

def update_dropdown():
    rules = load_rules()
    values = [f"{rule['ip']} ({rule['direction']})" for rule in rules['blocked_ips']]
    unblock_combo['values'] = values
    unblock_combo.set('')

# ------------------- GUI Code -------------------

root = tk.Tk()
root.title("Firewall Rule Manager")
root.geometry("800x700")
root.configure(bg="#F5F5F5")

root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

title_label = tk.Label(root, text="Windows Firewall Rule Manager", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="#333")
title_label.grid(row=0, column=0, pady=15, sticky="ew")

# Block Frame
block_frame = tk.LabelFrame(root, text="Block IP / Domain", bg="#ffffff", font=("Arial", 12))
block_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
block_frame.columnconfigure(1, weight=1)

tk.Label(block_frame, text="Enter IP / Domain:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ip_entry = tk.Entry(block_frame, font=("Arial", 12))
ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(block_frame, text="Select Block Direction:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", padx=10, pady=5)
block_type_var = tk.StringVar()
block_type_combo = ttk.Combobox(block_frame, textvariable=block_type_var, state="readonly",
                                 values=["IN", "OUT", "BOTH"], font=("Arial", 12), width=15)
block_type_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
block_type_combo.set("")

block_button = tk.Button(block_frame, text="Block", command=block_ip, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
block_button.grid(row=2, column=0, columnspan=2, pady=10)

# Unblock Frame
unblock_frame = tk.LabelFrame(root, text="Unblock IP", bg="#ffffff", font=("Arial", 12))
unblock_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
unblock_frame.columnconfigure(1, weight=1)

tk.Label(unblock_frame, text="Select IP to Unblock:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=10, pady=5)
unblock_combo = ttk.Combobox(unblock_frame, font=("Arial", 12), state="readonly")
unblock_combo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

unblock_button = tk.Button(unblock_frame, text="Unblock", command=unblock_ip, font=("Arial", 12), bg="#f44336", fg="white", width=15)
unblock_button.grid(row=1, column=0, columnspan=2, pady=10)

# Log Frame
log_frame = tk.LabelFrame(root, text="Command Log", bg="#ffffff", font=("Arial", 12))
log_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
log_frame.rowconfigure(0, weight=1)
log_frame.columnconfigure(0, weight=1)

log_text = scrolledtext.ScrolledText(log_frame, font=("Consolas", 11), wrap=tk.WORD)
log_text.grid(row=0, column=0, sticky="nsew")

# Status Bar
status_var = tk.StringVar()
status_var.set("Ready")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10), bg="#eeeeee")
status_bar.grid(row=4, column=0, sticky="ew")

update_dropdown()
root.mainloop()
