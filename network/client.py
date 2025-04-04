import socket
import threading

class Client:
    def __init__(self, server_ip="172.17.42.153", server_port=8000):
        self.server_address = (server_ip, server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.running = True
        self.on_message = None

    def send(self, message: str):
        if self.running:
            self.socket.sendto(message.encode(), self.server_address)

    def listen(self):
        def receive_loop():
            while self.running:
                try:
                    data, _ = self.socket.recvfrom(1024)
                    if self.on_message:
                        self.on_message(data.decode())
                except BlockingIOError:
                    pass
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] {e}")
                    break

        thread = threading.Thread(target=receive_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
        self.socket.close()