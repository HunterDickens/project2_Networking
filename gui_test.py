from gooey import Gooey, GooeyParser
import socket
import time

def ping(server_ip, server_port, a):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)
    if(a):
            client_socket.connect((server_ip,server_port))
            IPToCheck = client_socket.getpeername()
            name = socket.gethostbyaddr(IPToCheck[0])[0]
            print("Hostname: " + name)
    for sequence_number in range(1, 11):
        send_time = time.time()
        message = f'Ping {sequence_number} {send_time}'.encode()
        try:
            client_socket.sendto(message, (server_ip, server_port))
            modified_message, server_address = client_socket.recvfrom(1024)
            rtt = time.time() - send_time
            print(f"Sequence {sequence_number}: Reply from {server_address} RTT = {rtt:.3f}s")
        except socket.timeout:
            print(f"Sequence {sequence_number}: Request timed out")

    client_socket.close()

def tracert(server_ip, server_port, max_hops):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)
    print(f"Tracing route to {server_ip} over a maximum of {max_hops} hops:\n")

    for ttl in range(1, max_hops + 1):
        send_time = time.time()
        message = f'Tracert {ttl} {send_time}'.encode()
        try:
            client_socket.sendto(message, (server_ip, server_port))
            modified_message, server_address = client_socket.recvfrom(1024)
            rtt = time.time() - send_time
            print(f"Hop {ttl}: Reply from {server_address} RTT = {rtt:.3f}s")
        except socket.timeout:
            print(f"Hop {ttl}: Request timed out")

    client_socket.close()

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
