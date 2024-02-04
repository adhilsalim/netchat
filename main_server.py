import socket
import json
import threading

# Load clients' data from data.json
with open('data.json', 'r') as file:
    clients_data = json.load(file)
    clients_data = clients_data['systems']

# Server configuration
MAIN_SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
MAIN_SERVER_PORT = 65432    # Port to listen on
MAX_CLIENTS = 5             # Maximum number of clients
active_clients = {}         # Dictionary of active clients

# Return the username of the client
def get_username(ip_address):
    for client in clients_data:
        if client['ip'] == ip_address:
            return client['name']
    return 'Unknown'

def handle_client(client_socket, address):
    print(f"SYS: Handling {get_username(address[0])}")
    while True:
        try:
            # Get data from the client
            data = client_socket.recv(1024).decode()
            print(f"SYS: Received data from {get_username(address[0])}: {data}")
            # Decode JSON data
            message_data = json.loads(data)

            # If message is /close, close the connection
            if message_data['message'] == '/close':
                client_socket.close()
                break

            # Get message and IP address from the data
            message = message_data['message']
            ip_address = message_data['ip']
            ip_address = address[0]

            # Construct formatted message
            formatted_message = f"{get_username(ip_address)}: {message}"

            # Send the message to all active clients
            for other_ip, other_client_socket in active_clients.items():
                try:
                    other_client_socket.sendall(formatted_message.encode())
                except Exception as e:
                    print(f"Error sending message to {get_username(other_ip)}: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {str(e)}")
        except Exception as e:
            print(f"Error receiving message from {get_username(address[0])}: {str(e)}")
            break
    # Close the client socket
    client_socket.close()
    del active_clients[address[0]]
    print(f"Connection with {get_username(address[0])} closed")

# Main function
def main():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("SYS: Main server socket created")
    server_socket.bind((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    print("SYS: Main server socket bound")
    server_socket.listen(MAX_CLIENTS)
    print(f"SYS: Server is listening on {MAIN_SERVER_IP}:{MAIN_SERVER_PORT}")

    while True:
        # Accept new connections
        print("SYS: Waiting for new connection...")
        client_socket, address = server_socket.accept()
        print(f"SYS: New connection from ({address[0]}:{address[1]}) as {get_username(address[0])}")

        # Add the new client to the active clients dictionary
        active_clients[address[0]] = client_socket
        print(f"SYS: Active clients: {len(active_clients)}")

        # Create a new thread to handle the new client
        print(f"SYS: Starting new thread for {get_username(address[0])}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        print(f"SYS: Thread for {get_username(address[0])} started")
        client_thread.start()

# Starting point of the program
if __name__ == '__main__':
    print("SYS: Starting server...")
    main()