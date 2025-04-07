import socket

class Server:
    def __init__(self, host="172.17.42.153", port=8000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        print(f"[SERVER STARTED] Listening on {host}:{port}")
        self.players = []

    def start(self):
        while True:
            data, addr = self.server_socket.recvfrom(1024)
            message = data.decode()
            if addr not in self.players:
                if len(self.players) < 2:
                    self.players.append(addr)
                    print(f"[PLAYER CONNECTED] {addr}")
                else:
                    print(f"[REJECTED] {addr} (room full)")
                    continue

            print(f"[RECEIVED] {message} from {addr}")

            # Send message to the other player
            for player in self.players:
                if player != addr:
                    self.server_socket.sendto(data, player)

if __name__ == "__main__":
    server = Server()
    server.start()
