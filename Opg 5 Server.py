from socket import *
import json
import random
import threading

def process_request(request):
    try:
        method = request["method"]

        if method == 'Random':
            tal1 = request.get("Tal1", 0)
            tal2 = request.get("Tal2", 0)
            result = random.randint(min(tal1, tal2), max(tal1, tal2))
        elif method == 'Add':
            tal1 = request.get("Tal1", 0)
            tal2 = request.get("Tal2", 0)
            result = tal1 + tal2
        elif method == 'Subtract':
            tal1 = request.get("Tal1", 0)
            tal2 = request.get("Tal2", 0)
            result = tal1 - tal2
        else:
            return {"error": "Invalid method"}

        return {"result": result}

    except KeyError:
        return {"error": "Invalid request format"}

def client_thread(connection_socket, addr):
    try:
        print(f'Connection established with {addr}')
        data = connection_socket.recv(1024).decode()

        try:
            request = json.loads(data)
            response = process_request(request)
        except json.JSONDecodeError:
            response = {"error": "Invalid JSON format"}

        connection_socket.send(json.dumps(response).encode())
    finally:
        connection_socket.close()
        print(f'Connection closed with {addr}')

def start_server():
    server_port = 12000

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen()

    print(f"Server listening on port {server_port}")

    while True:
        connection_socket, addr = server_socket.accept()
        threading.Thread(target=client_thread, args=(connection_socket, addr)).start()

if __name__ == "__main__":
    start_server()
