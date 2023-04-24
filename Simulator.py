import zmq
import multiprocessing as mp
from LoadBalancer import *
from Server import *
from termcolor import colored

# Define a function that will run in a separate process
def client_process():
    # Create a ZeroMQ context and socket, and connect to the load balancer
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    lb_addr = "tcp://localhost:5555"
    print(colored(f"Client connecting to {lb_addr}.", "yellow"))
    socket.connect(lb_addr)
    print(colored(f"Client connecting to {lb_addr} was successful.", "yellow"))

    # Send five requests to the load balancer and print the responses
    for request in range(5):
        print(colored("CLIENT: Sending message: Hello", "yellow"))
        socket.send(b"Hello")

        print(colored("CLIENT: waiting for response", "yellow"))
        message = socket.recv()
        print(colored(f"CLIENT: Received reply {request}: {message.decode()}", "yellow"))

# Define a function that will run in a separate process
def server_process(addr):
    # Create a new instance of the Server class with the specified address
    server = EchoServer(addr)
    server.run()

if __name__ == "__main__":
    print(f"__name___ == __main__.")

     # Start the load balancer in a separate thread
    frontend_addr = "tcp://*:5555"
    backend_addrs = ["tcp://localhost:5560", "tcp://localhost:5561"]
    lb = LoadBalancer(frontend_addr, backend_addrs)
    lb_thread = threading.Thread(target=lb.run)
    lb_thread.start()
    
    print(f"Load Balancer running at {frontend_addr} with backends at .")

    # Start five instances of the EchoServer subclass in separate processes
    num_servers = 2
    processes = []
    for i in range(num_servers):
        addr = f"556{i}"
        print(f"Server Process running at {addr}.")
        process = mp.Process(target=server_process, args=(addr,))
        processes.append(process)
        process.start()

    #Start two instances of the client process
    for i in range(2):
        process = mp.Process(target=client_process)
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    print("Waiting for processes to complete.")
    for process in processes:
        process.join()