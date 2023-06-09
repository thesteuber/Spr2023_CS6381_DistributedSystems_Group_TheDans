import zmq
from termcolor import colored

class LoadBalancer:
    def __init__(self, frontend_addr, backend_addrs):
        # Set up the ZeroMQ sockets for the frontend and backend
        self.context = zmq.Context.instance()
        self.frontend_socket = self.context.socket(zmq.ROUTER)
        self.backend_socket = self.context.socket(zmq.DEALER)
        
        # Bind the frontend socket to the specified address
        self.frontend_socket.bind(frontend_addr)
        
        # Connect the backend socket to each of the specified server addresses
        for addr in backend_addrs:
            self.backend_socket.connect(addr)
        
        # Set up the load balancing state
        self.server_count = len(backend_addrs)
        self.next_server = 0
    
    def run(self):
        # Loop indefinitely, waiting for incoming messages and forwarding them to servers
        while True:
            # Receive a message from the frontend socket and forward it to a backend socket
            # message = self.frontend_socket.recv_multipart()
            # Split up what we receive from the client into a client_id, ????, and the message
            # It has 3 parts?
            client_id, var, message = self.frontend_socket.recv_multipart()

            # print("FLAG 1")
            # print(client_id)
            # print(message)
            # print(var)

            server_id = self.next_server % self.server_count
            # self.backend_socket.send_multipart([bytes(str(server_id), "utf-8"), b"", bytes(message[0])])
            self.backend_socket.send_multipart([bytes(str(server_id), "utf-8"), b"", bytes(message)])
            print(colored(f"Load balancer sent message to server {server_id}", "blue"))
            self.next_server += 1

            # Receive a message from a backend socket and forward it to the frontend socket
            print(colored(f"Load balancer listening for message from server {server_id}", "blue"))
            server_id, _, message = self.backend_socket.recv_multipart()
            print(colored(f"Load balancer message received from server {message}", "blue"))

            # Send the message back to the client, including the client identity
            # client_id, message = message[:2]
            # self.frontend_socket.send_multipart([bytes(str(client_id), "utf-8"), b"", bytes(message[0])])
            self.frontend_socket.send_multipart([client_id, b"", message])

            # Send the message back to the client
            # self.frontend_socket.send_multipart([message])
            print(colored(f"Load balancer message relayed to client {message} successfully", "blue"))