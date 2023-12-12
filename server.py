import socket
import time

HOST = '0.0.0.0'
PORT = 65432

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            handle_client(client_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        
        print(f"{time.strftime('%H:%M:%S')}: {data}")

        if data == "/close":
            break

if __name__ == '__main__':
    main()
