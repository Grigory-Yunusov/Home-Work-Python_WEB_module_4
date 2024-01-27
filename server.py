import socket


def main():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    conn, addr = server_socket.accept()

    print('soccket from', addr)

    while True:
        data = conn.recv(1024)
        print('data',data)
        if data.decode() == 'pass_me':
            print(data)
            conn.send('you passed security check'.encode())

            if not data:
                break
        else: break

    conn.close()

if __name__ == '__main__':
    main()
