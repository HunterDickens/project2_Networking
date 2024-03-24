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

    # Simulate network delay
    time.sleep(random.random() * .2)

    # Respond only if rand is less than 7, simulating 70% response rate
    if rand < 7:
        server_socket.sendto(message, address)


