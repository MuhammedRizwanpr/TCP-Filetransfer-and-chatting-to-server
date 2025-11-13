import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '192.168.56.140'
PORT = 12345
client_socket.connect((HOST, PORT))
print("Connected to the server!")

def chat_server():
    while True:
        message = input("Client: ")
        if message.lower() == 'exit':
            print("Closing connection.")
            break
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print("Server says:", data.decode())

def file_transfer():
    filenames = client_socket.recv(1024).decode()
    filename = input(f"Available files: {filenames}\nEnter filename to download: ")
    client_socket.sendall(filename.encode())  # <-- send chosen filename

    with open(f"new_{filename}", "wb") as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print("File downloaded successfully!")

print("1. Download file from server\n2. Chat with server")
choice = input("Enter 1 or 2: ")
client_socket.sendall(choice.encode())

if choice == "2":
    chat_server()
elif choice == "1":
    file_transfer()

client_socket.close()
