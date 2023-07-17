import socket

def main():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the subprocess
    s.connect(('localhost', 5000))

    # Send data to the subprocess
    data = "Hello from Python 2.7!"
    s.sendall(data.encode())

    # Receive data from the subprocess
    response = s.recv(1024)
    print(response.decode())

    # Close the socket
    s.close()

if __name__ == '__main__':
    main()