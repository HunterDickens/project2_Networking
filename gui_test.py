from gooey import Gooey, GooeyParser
import socket
import time

def ping(server_ip, server_port, a):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket timeout for 1 second
    client_socket.settimeout(.5)
    counter = 0
    lost = 0

    if(a):
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
