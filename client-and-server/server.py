import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '0.0.0.0'   # listen on all interfaces
PORT = 12345
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

def chat_server():
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Client says:", data.decode())
        response = input("Server reply: ")
        if response.lower() == "exit":
            break
        conn.sendall(response.encode())

def file_transfer():
    files = "sample1.txt, sample2.txt"
    conn.sendall(files.encode())  # send file list
    filename = conn.recv(1024).decode().strip()
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            chunk = f.read(1024)
            while chunk:
                conn.sendall(chunk)
                chunk = f.read(1024)
        print("File sent successfully!")
    else:
        print("File not found!")

choice = conn.recv(1024).decode()
if choice == "1":
    file_transfer()
elif choice == "2":
    chat_server()

conn.close()
server_socket.close()
print("Server closed connection.")
