import socket
import time
import sys

server_port = 12000

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket timeout for 1 second
client_socket.settimeout(.5)
argsCount = len(sys.argv)
server_ip = sys.argv[1]
counter = 0
lost = 0

if(argsCount > 1):
    if "-a" in sys.argv:
        client_socket.connect((server_ip,server_port))
        IPToCheck = client_socket.getpeername()
        name = socket.gethostbyaddr(IPToCheck[0])[0]
        print("Hostname: " + name)
# Ping for 10 pings
message = bytes("9c$&gK!2z@%R7*BpH@XvY3gfE6^+aUQw", "utf-8")
totalTime = 0
array = []
numOfPings = 4
for sequence_number in range(1,(numOfPings+1)):

    #32 byte string
    try:
        send_time = time.time()*1000.0
        # Send the ping message
        client_socket.sendto(message, (server_ip, server_port))
        # Receive the server response
        modified_message, server_address = client_socket.recvfrom(1024)
        rtt = (time.time()*1000.0) - send_time
        totalTime += rtt
        array.append(rtt)
        print(f"Sequence {sequence_number}: Reply from {server_address} RTT = {rtt:.0f} ms Bytes: {len(message)}")
        counter+=1
    except socket.timeout:
        print(f"Sequence {sequence_number}: Request timed out")
        lost+=1

# Close the socket
client_socket.close()
print("Ping Statistics for " + server_ip)
print("\tPackets: sent = 4, Recieved = " + str(counter) + " lost = " + str(lost) + " (" + str(int(((1-counter/(counter+lost)))*100)) + "% loss)")
print("Approximate round trip time in milli-seconds:")
minimum = 1000000
maximum = 0
for i in array:
    if i < minimum:
        minimum = i
    if i > maximum:
        maximum = i
average = totalTime/numOfPings
print(f"\tMinimum: {minimum:.0f} ms, Maximum: {maximum:.0f} ms, Average = {average:.0f} ms Bytes")
