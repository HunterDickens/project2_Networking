import socket
import time

# Server address and port
server_ip = '127.0.0.1'
server_port = 12000

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket timeout for 1 second
client_socket.settimeout(1)

# Maximum hops to simulate
max_hops = 30

print(f"Tracing route to {server_ip} over a maximum of {max_hops} hops:\n")

for ttl in range(1, max_hops + 1):
    send_time = time.time()
    message = 'tracingRoute'.encode()

    try:
        # Send the "tracert" message with simulated TTL
        client_socket.sendto(message, (server_ip, server_port))
        # Receive the server response
        modified_message, server_address = client_socket.recvfrom(1024)
        rtt = time.time() - send_time
        print(f"Hop {ttl}: Reply from {modified_message.decode()} RTT = {rtt:.3f}s")
    except socket.timeout:
        print(f"Hop {ttl}: Request timed out")

# Close the socket
client_socket.close()
