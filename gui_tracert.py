import tkinter as tk
from tkinter import scrolledtext
import socket
import time

class TracerouteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simulated Tracert")

        # Server IP Entry
        tk.Label(master, text="Server IP:").pack(pady=5)
        self.ip_entry = tk.Entry(master)
        self.ip_entry.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(master, text="Start Tracert", command=self.start_tracert)
        self.start_button.pack(pady=10)
        print("Tracing route to")

        # Output Area
        self.output_text = scrolledtext.ScrolledText(master, width=70, height=20)
        self.output_text.pack(pady=5)

        # UDP Socket Setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1)

    def start_tracert(self):
        server_ip = self.ip_entry.get()
        if not server_ip:
            self.output_text.insert(tk.INSERT, "Please enter a server IP address.\n")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, f"Tracing route to {server_ip} over a maximum of 30 hops:\n\n")
        max_hops = 30

        for ttl in range(1, max_hops + 1):
            send_time = time.time()
            message = f'Tracert {ttl} {send_time}'.encode()
            try:
                self.client_socket.sendto(message, (server_ip, 12000))
                _, server_address = self.client_socket.recvfrom(1024)
                rtt = time.time() - send_time
                self.output_text.insert(tk.INSERT, f"Hop {ttl}: Reply from {server_address} RTT = {rtt:.3f}s\n")
            except socket.timeout:
                self.output_text.insert(tk.INSERT, f"Hop {ttl}: Request timed out\n")

    def close_socket(self):
        self.client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    gui = TracerouteGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.close_socket)
    root.mainloop()

