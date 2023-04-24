import zmq
import threading

class Server:
    def __init__(self, addr):
        # Set up the ZeroMQ socket to listen on the specified address
        self.addr = addr
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        print(f"Server binding to socket at: {self.addr}")
        self.socket.bind("tcp://*:{}".format(self.addr))
        print(f"Server binding to socket at: {self.addr} was successful")

    def run(self):
        # Loop indefinitely, waiting for incoming messages and handling them
        while True:
            print(f"Server listening at: {self.addr}")
            message = self.socket.recv()
            response = self.handle_message(message)
            self.socket.send(response)

    def handle_message(self, message):
        # This method should be overridden by a subclass to handle the message
        return b""

class EchoServer(Server):
    def handle_message(self, message):
        # This subclass simply echoes back the message it receives
        return message

def start_servers(num_servers):
    threads = []
    for i in range(num_servers):
        # Create a new instance of the EchoServer subclass with a unique address
        server = EchoServer(f"tcp://*:555{i}")
        # Create a new thread to run the server instance
        thread = threading.Thread(target=server.run)
        # Start the thread and add it to the list of threads
        thread.start()
        threads.append(thread)
    return threads

if __name__ == "__main__":
    # Start five instances of the EchoServer subclass
    num_servers = 5
    threads = start_servers(num_servers)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()