import socket

HOST = '192.168.1.4'
PORT = 65432

def send_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    while True:
        message = input("Enter message to send (type '/close' to exit): ")
        send_message(message)
        if message == "/close":
            break
