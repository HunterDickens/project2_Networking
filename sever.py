import socket
import random
import time

# Server settings
server_ip = '127.0.0.1'
server_port = 12000
buffer_size = 32

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print("The server is ready to receive on port:", server_port)

while True:
    # Generate a random number to simulate packet loss
    rand = random.randint(1, 10)
    message, address = server_socket.recvfrom(buffer_size)
    if message == 'tracingRoute'.encode():
        randomIp = random.randint(0,49)
        ips = [
        "192.168.0.1", "10.0.0.1", "172.16.0.1", "192.168.1.1", "192.168.100.1",
        "192.168.2.1", "192.168.10.1", "192.168.11.1", "192.168.20.1", "192.168.30.1",
        "192.168.40.1", "192.168.50.1", "192.168.60.1", "192.168.70.1", "192.168.80.1",
        "192.168.90.1", "192.168.100.1", "192.168.110.1", "192.168.120.1", "192.168.130.1",
        "192.168.140.1", "192.168.150.1", "192.168.160.1", "192.168.170.1", "192.168.180.1",
        "192.168.190.1", "192.168.200.1", "192.168.210.1", "192.168.220.1", "192.168.230.1",
        "192.168.240.1", "192.168.250.1", "192.168.0.2", "192.168.1.2", "192.168.2.2",
        "192.168.3.2", "192.168.4.2", "192.168.5.2", "192.168.6.2", "192.168.7.2", "192.168.8.2",
        "192.168.9.2", "192.168.10.2", "192.168.11.2", "192.168.12.2", "192.168.13.2", "192.168.14.2",
        "192.168.15.2", "192.168.16.2", "192.168.17.2"
        ]
        message = ips[randomIp].encode()
    # Simulate network delay
    time.sleep(random.random() * .2)

    # Respond only if rand is less than 7, simulating 70% response rate
    if rand < 7:
        server_socket.sendto(message, address)


