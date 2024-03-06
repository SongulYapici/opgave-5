from socket import *
import json

def get_server_response(client_socket):
    return client_socket.recv(1024).decode()

server_name = "localhost"
server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

command = input("Enter the command (Random, Add, Subtract): ")
tal1 = int(input("Enter the first number: "))
tal2 = int(input("Enter the second number: "))

request = {"method": command, "Tal1": tal1, "Tal2": tal2}
client_socket.send(json.dumps(request).encode())

response_data = json.loads(get_server_response(client_socket))

if "error" in response_data:
    print(f"Server error: {response_data['error']}")
elif "result" in response_data:
    print(f'Result from server: {response_data["result"]}')

client_socket.close()
