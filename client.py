import socket
import time
import sys

# Server address and port
#server_ip = '127.0.0.1'
server_port = 12000

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket timeout for 1 second
client_socket.settimeout(2)
argsCount = len(sys.argv)
server_ip = sys.argv[1]
#print("test" + server_ip + "test")
if(argsCount > 1):
    if "-a" in sys.argv:
        client_socket.connect((server_ip,server_port))
        IPToCheck = client_socket.getpeername()
        name = socket.gethostbyaddr(IPToCheck[0])[0]
        print("Hostname: " + name)
# Ping for 10 pings
for sequence_number in range(1, 11):
    send_time = time.time()
    message = f'Ping {sequence_number} {send_time}'.encode()
    try:
        # Send the ping message
        client_socket.sendto(message, (server_ip, server_port))
        # Receive the server response
        modified_message, server_address = client_socket.recvfrom(1024)
        rtt = time.time() - send_time
        print(f"Sequence {sequence_number}: Reply from {server_address} RTT = {rtt:.3f}s")
    except socket.timeout:
        print(f"Sequence {sequence_number}: Request timed out")

# Close the socket
client_socket.close()
