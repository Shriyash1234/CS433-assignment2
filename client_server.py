import socket
import argparse
import time
import random
import string

def generate_random_data():
    length = 10000
    # Generate random string of length 'length'
    random_data = ''.join('qyfyfhasgjbjhasjghjKHMQWDLQDqwwd'*length)
    return random_data

def client(server_ip, server_port, congestion_control):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, congestion_control.encode())
    client_socket.connect((server_ip, server_port))
    print(f"Connected Server: {server_ip}:{server_port} Congestion Algorithm: {congestion_control}")

    while True:
        data = generate_random_data()
        client_socket.sendall(data.encode())
        time.sleep(1)
    
def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    print(f"Port :- {port}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP client and Server Program')
    parser.add_argument('--r', choices=['server', 'client'], required=True)
    parser.add_argument('--c', choices=['vegas', 'reno', 'cubic', 'bbr'], required=True)
    parser.add_argument('--config', choices=['b', 'c'], required=True)
    parser.add_argument('--p', type=int, required=True)
    
    args = parser.parse_args()

    if args.r == 'server':
        server(args.p)
    elif args.r== 'client':
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(hostname, ip)
        if args.config == 'b' and ip == '10.0.0.1':
            client('10.0.0.4', args.p, args.c)
        elif args.config == 'c':
            client('10.0.0.4', args.p, args.c)