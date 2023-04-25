import zmq
import multiprocessing as mp
from LoadBalancer import *
from Server import *
from termcolor import colored
import datetime

def write_latency_row(time_sent, filename):
    f = open(filename, "a")
    time_received = datetime.datetime.now().isoformat(sep=" ")
    time_elapsed = (datetime.datetime.fromisoformat(time_received) - datetime.datetime.fromisoformat(time_sent)).microseconds / 1000
    f.write(time_sent + "," + time_received + "," + str(time_elapsed) + "\n")
    f.close()

# Define a function that will run in a separate process
def client_process(output_file, lb_port, messages_per_client):
    # Create a ZeroMQ context and socket, and connect to the load balancer
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    lb_addr = f"tcp://localhost:{lb_port}"
    print(colored(f"Client connecting to {lb_addr}.", "yellow"))
    socket.connect(lb_addr)
    print(colored(f"Client connecting to {lb_addr} was successful.", "yellow"))

    # Send five requests to the load balancer and print the responses
    for request in range(messages_per_client):
        print(colored("CLIENT: Sending message: Hello", "yellow"))
        time_sent = datetime.datetime.now().isoformat(sep=" ")
        socket.send(b"Hello")

        print(colored("CLIENT: waiting for response", "yellow"))
        message = socket.recv()
        print(colored(f"CLIENT: Received reply {request}: {message.decode()}", "yellow"))
        write_latency_row(time_sent, output_file)

# Define a function that will run in a separate process
def server_process(addr):
    # Create a new instance of the Server class with the specified address
    server = EchoServer(addr)
    server.run()

if __name__ == "__main__":
    print(f"__name___ == __main__.")

    num_load_balancers = 10
    num_clients = 100
    num_servers = 50
    messages_per_client = 20

    backend_addrs = []
    for i in range(num_servers):
        backend_addrs.append(f"tcp://localhost:556{i}")

    lb_ports = []
    for j in range(num_load_balancers):
        # Start the load balancer in a separate thread
        port = f"500{j}"
        frontend_addr = f"tcp://*:{port}"
        lb_ports.append(port)
        lb = LoadBalancer(frontend_addr, backend_addrs)
        lb_thread = threading.Thread(target=lb.run)
        lb_thread.start()
    
    print(f"Load Balancer running at {frontend_addr} with backends at .")

    f = open("output.csv", "w+")
    f.write("time_sent,time_received,time_elapsed\n")
    f.close()

    # Start five instances of the EchoServer subclass in separate processes
    
    processes = []
    for i in range(num_servers):
        addr = f"556{i}"
        print(f"Server Process running at {addr}.")
        process = mp.Process(target=server_process, args=(addr,))
        processes.append(process)
        process.start()

    #Start two instances of the client process
    clients_initialized = 0
    for i in range(num_clients):
        process = mp.Process(target=client_process, args=("output.csv", lb_ports[clients_initialized % len(lb_ports)], messages_per_client,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    print("Waiting for processes to complete.")
    for process in processes:
        process.join()