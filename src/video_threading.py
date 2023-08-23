# Camera capture program for running this application without Nao.
# If with a real Nao, this python file will not be ran.
import cv2
import socket
import sys


def start_threading():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return
    return cap


def take_picture(cap, path):
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture the photo.")
        cap.release()
        return
    frame = cv2.resize(frame, (160, 120))
    cv2.imwrite(path, frame)


def stop_threading(cap):
    cap.release()


def connect_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))
    return s


def main(path, socket_enable=True):
    if not socket_enable:  # for testing sub functions
        cap = start_threading()
        take_picture(cap, path)
        stop_threading(cap)
    else:
        s = connect_socket(int(sys.argv[1]))
        while True:
            response = s.recv(1024)
            print(response.decode())
            if response.decode() == 'quit':
                try:
                    stop_threading(cap)
                except:
                    print('No opening camera need to be close')
                s.close()
                exit()
            if response.decode() == 'camera_open':
                cap = start_threading()
                if cap.isOpened():
                    s.sendall('camera_opened'.encode())
                else:
                    s.sendall('camera_open_failed'.encode())
                    break
            if response.decode() == 'take_picture':
                try:
                    take_picture(cap, path)
                    s.sendall('picture_took'.encode())
                except:
                    print('No camera exists')
                    s.sendall('picture_took_failed'.encode())


if __name__ == '__main__':
    path = './recordings/pictures/tmp_image.jpg'
    main(path, False)
