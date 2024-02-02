import socket
import json

# Load username and IP address from local storage (replace with your method)
with open("user_info.json", "r") as f:
    user_info = json.load(f)

username = user_info["username"]
ip_address = user_info["ip"]

# Server IP and port
SERVER_IP = "127.0.0.1"  # Replace with the actual server IP
SERVER_PORT = 65432

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((SERVER_IP, SERVER_PORT))

print(f"Connected to server as {username} ({ip_address})")

while True:
    # Get message input from user
    message = input("Enter your message: ")

    # Create message data with username and IP
    message_data = {"message": message, "ip": ip_address}

    # Send message data to server
    client_socket.sendall(json.dumps(message_data).encode())

    # Receive and display messages from server
    data = client_socket.recv(1024).decode()
    if data:
        print(f"{data}")

    # Check for exit command
    if message == "/exit":
        break

# Close socket
client_socket.close()
print("Disconnected from server")
