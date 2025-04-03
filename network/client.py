import socket
import threading

class Client:
    def __init__(self, server_ip="localhost", server_port=8000):
        self.server_address = (server_ip, server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = True
        self.on_message = None

    def send(self, message: str):
        self.socket.sendto(message.encode(), self.server_address)

    def listen(self):
        def receive_loop():
            while self.running:
                try:
                    data, _ = self.socket.recvfrom(1024)
                    if self.on_message:
                        self.on_message(data.decode())
                except Exception as e:
                    print(f"[ERROR] {e}")
                    break

        thread = threading.Thread(target=receive_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
        self.socket.close()
