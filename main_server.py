import socket
import json
import threading

# load clients data from data.json
with open('data.json', 'r') as file:
    clients_data = json.load(file)

# server configuration
MAIN_SERVER_IP = '0.0.0.0'  # listen on all available interfaces
MAIN_SERVER_PORT = 65432    # port to listen on
MAX_CLIENTS = 5 # maximum number of clients
active_clients = {} # dictionary of active clients

# return the username of the client
def getUsername(ip_address):
    for client in clients_data:
        if client['ip'] == ip_address:
            return client['name']
    return 'Unknown'


def handleClient(client_socket, address):
    while True:
        try:
            # get data from the client
            data = client_socket.recv(1024).decode()

            # if data is /close, close the connection
            if data == '/close':
                client_socket.close()
                break

            # decode json data
            message_data = json.loads(data)

            # get message and ip address from the data
            message = message_data['message']
            ip_address = message_data['ip']
            ip_address = address[0]

            # construct formatted message
            formatted_message = f"{getUsername(ip_address)}: {message}"

            # send the message to all active clients
            for other_client_socket, other_address in active_clients.items():
                if other_address != address:
                    try:
                        other_client_socket.sendall(formatted_message.encode())
                    except:
                        print(f"Error sending message to {getUsername(other_address[0])}")
        except:
            print(f"Error receiving message from {getUsername(address[0])}")
            break
    # close the client socket
    client_socket.close()
    del active_clients[address[0]]
    print(f"Connection with {getUsername(address[0])} closed")

# main function
def main():

    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    server_socket.listen(MAX_CLIENTS)

    print(f"Server is listening on {MAIN_SERVER_IP}:{MAIN_SERVER_PORT}")

    while True:
        # accept new connections
        client_socket, address = server_socket.accept()
        print(f"New connection from ({address[0]}:{address[1]}) as {getUsername(address[0])}")

        # add the new client to the active clients dictionary
        active_clients[address[0]] = client_socket

        # create a new thread to handle the new client
        client_thread = threading.Thread(target=handleClient, args=(client_socket, address))
        client_thread.start()

# starting point of the program
if __name__ == '__main__':
    main()