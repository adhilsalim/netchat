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
    print(f"Handling {get_username(address[0])}")
    while True:
        try:
            # Get data from the client
            data = client_socket.recv(1024).decode()

            # If data is /close, close the connection
            if data == '/close':
                client_socket.close()
                break

            # Decode JSON data
            message_data = json.loads(data)

            # Get message and IP address from the data
            message = message_data['message']
            ip_address = message_data['ip']
            ip_address = address[0]

            # Construct formatted message
            formatted_message = f"{get_username(ip_address)}: {message}"

            # Send the message to all active clients
            for other_client_socket, other_address in active_clients.items():
                if other_address != address:
                    try:
                        other_client_socket.sendall(formatted_message.encode())
                    except Exception as e:
                        print(f"Error sending message to {get_username(other_address[0])}: {str(e)}")
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
    print("Main server socket created")
    server_socket.bind((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    print("Main server socket bound")
    server_socket.listen(MAX_CLIENTS)
    print(f"Server is listening on {MAIN_SERVER_IP}:{MAIN_SERVER_PORT}")

    while True:
        # Accept new connections
        print("Waiting for new connection...")
        client_socket, address = server_socket.accept()
        print(f"New connection from ({address[0]}:{address[1]}) as {get_username(address[0])}")

        # Add the new client to the active clients dictionary
        active_clients[address[0]] = client_socket
        print(f"Active clients: {len(active_clients)}")

        # Create a new thread to handle the new client
        print(f"Starting new thread for {get_username(address[0])}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        print(f"Thread for {get_username(address[0])} started")
        client_thread.start()

# Starting point of the program
if __name__ == '__main__':
    print("Starting server...")
    main()