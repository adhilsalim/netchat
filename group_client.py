import socket
import json

# Load username and IP address from local storage (replace with your method)
username = "Lap-1"
ip_address = "192.168.1.4"  # Temporary IP address for testing

# Server IP and port
SERVER_IP = "192.168.1.4"  # Replace with the actual server IP
SERVER_PORT = 65432

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((SERVER_IP, SERVER_PORT))

print(f"Connected to server as {username} ({ip_address})")

try:
    while True:
        # Get message input from user
        message = input("Enter your message: ")

        # Create message data with username and IP
        message_data = {"message": message, "ip": ip_address}

        # Send message data to server
        client_socket.sendall(json.dumps(message_data).encode())

        # Check for exit command
        if message == "/exit":
            break

        # Receive and display messages from server
        data = client_socket.recv(1024).decode()
        if data:
            print(f"{data}")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close socket
    client_socket.close()
    print("Disconnected from server")
