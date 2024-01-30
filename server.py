# import json
# import socket


# UDP_IP = '127.0.0.1'
# UDP_PORT = 5000


# def run_server(ip, port):
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
#         server = ip, port
#         sock.bind(server)
#         try:
#             while True:
#                 data, address = sock.recvform(1024)
#                 print(f"Received data: {data.decode()} to server: {server}")
#                 data_dict = json.loads(data.decode())
#                 with open('storage/data.json', 'a') as file:
#                     json.dump(data_dict, file, indent=2)
#                 sock.sendto(data, address)
#                 print(f"Sent data: {data.decode()} to: {address}")
#         except KeyboardInterrupt:
#             print(f'Destroy server')
#             raise
#         finally:
#             print('Closing server socket')

# if __name__ == '__main__':
#      run_server(UDP_IP, UDP_PORT)





















respont, address = sock.recvform(1024)
            print(f"Received data: {respont.decode()} from address: {address}")