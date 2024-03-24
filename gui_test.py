from gooey import Gooey, GooeyParser
import socket
import time
import socket
import subprocess
import platform
import random


def ping(server_ip, server_port, a):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(.5)
    counter = 0
    lost = 0

    if a:
        try:
            name = socket.gethostbyaddr(server_ip)[0]
        except socket.herror:
            name = "Hostname could not be resolved"
        print("Hostname: " + name)


    message = bytes("9c$&gK!2z@%R7*BpH@XvY3gfE6^+aUQw", "utf-8")
    totalTime = 0
    array = []
    numOfPings = 4
    for sequence_number in range(1,(numOfPings+1)):

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

pass

def tracert(server_ip, server_port, max_hops):
    # Check if we're in simulation mode
    if server_ip == "127.0.0.1":
        # Simulate tracerouting for demonstration purposes
        print(f"Simulated Tracerouting with a maximum of {max_hops} hops:\n")
        for hop in range(1, max_hops + 1):
            router_ip = f"192.168.0.{hop}"
            rtt1 = round(random.uniform(10, 100), 2)
            rtt2 = round(random.uniform(10, 100), 2)
            rtt3 = round(random.uniform(10, 100), 2)
            print(f"{hop} {router_ip}  {rtt1} ms  {rtt2} ms  {rtt3} ms")
    else:
        # Perform real traceroute operation
        command = ['traceroute', '-m', str(max_hops)] if platform.system().lower() != 'windows' else ['tracert', '-h', str(max_hops)]
        command.append(server_ip)  # Append the target IP address/host to the command
        
        try:
            print(f"Tracerouting to {server_ip} with a maximum of {max_hops} hops:\n")
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, shell=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute traceroute: {e.output}")



@Gooey(program_name="Network Utilities", default_size=(600, 400))
def main():
    parser = GooeyParser(description="Simulated Ping and Traceroute")
    subparsers = parser.add_subparsers(help='commands', dest='command')

    ping_parser = subparsers.add_parser('ping')
    ping_parser.add_argument('server_ip', type=str, help='Server IP Address')
    ping_parser.add_argument('server_port', type=int, help='Server Port')
    parser.add_argument('-a',
                        widget='CheckBox',
                        default = False,
                        action = "store_true",
                        help='Resolve address to hostname')
    ping_parser.add_argument('-a', action='store_true', help = 'resolve addresses to hostname')

    tracert_parser = subparsers.add_parser('tracert')
    tracert_parser.add_argument('server_ip', type=str, help='Server IP Address')
    tracert_parser.add_argument('server_port', type=int, help='Server Port')
    tracert_parser.add_argument('max_hops', type=int, help='Maximum Hops')

    args = parser.parse_args()

    if args.command == 'ping':
        ping(args.server_ip, args.server_port, args.a)
    elif args.command == 'tracert':
        tracert(args.server_ip, args.server_port, args.max_hops)

if __name__ == "__main__":
    main()
