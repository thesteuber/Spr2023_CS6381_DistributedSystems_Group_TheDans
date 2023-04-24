import zmq

class LoadBalancer:
    def __init__(self, frontend_addr, backend_addr):
        # Set up the frontend and backend addresses
        self.frontend_addr = frontend_addr
        self.backend_addr = backend_addr
        # Create a ZeroMQ context and sockets for the frontend and backend
        self.context = zmq.Context()
        self.frontend_socket = self.context.socket(zmq.ROUTER) # ROUTER socket for the frontend
        self.backend_socket = self.context.socket(zmq.DEALER) # DEALER socket for the backend
        # Bind the sockets to the specified addresses
        self.frontend_socket.bind(self.frontend_addr)
        self.backend_socket.bind(self.backend_addr)

    def run(self):
        # Create a ZeroMQ poller and register the frontend and backend sockets
        poller = zmq.Poller()
        poller.register(self.frontend_socket, zmq.POLLIN)
        poller.register(self.backend_socket, zmq.POLLIN)
        # Loop indefinitely, processing incoming messages
        while True:
            # Poll the sockets for incoming messages
            sockets = dict(poller.poll())
            # If there's a message on the frontend socket, forward it to the backend socket
            if self.frontend_socket in sockets:
                message = self.frontend_socket.recv_multipart()
                self.backend_socket.send_multipart(message)
            # If there's a message on the backend socket, forward it to the frontend socket
            if self.backend_socket in sockets:
                message = self.backend_socket.recv_multipart()
                self.frontend_socket.send_multipart(message)