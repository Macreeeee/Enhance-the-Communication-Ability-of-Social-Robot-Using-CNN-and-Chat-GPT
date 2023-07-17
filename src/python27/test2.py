import socket

def main():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    s.bind(('localhost', 5000))

    # Listen for incoming connections
    s.listen(1)

    # Accept a connection from the parent process
    conn, addr = s.accept()

    # Receive data from the parent process
    data = conn.recv(1024)
    print(data.decode())

    # Send data back to the parent process
    response = "Hello from Python 3.x!"
    conn.sendall(response.encode())

    # Close the connection and socket
    conn.close()
    s.close()

if __name__ == '__main__':
    main()