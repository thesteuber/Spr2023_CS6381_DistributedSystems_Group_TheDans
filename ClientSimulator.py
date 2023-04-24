import multiprocessing as mp
import zmq


# Define a function that will run in a separate process
def client_process():
    # Create a ZeroMQ context and socket, and connect to the load balancer
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Send five requests to the load balancer and print the responses
    for request in range(5):
        socket.send(b"Hello")
        message = socket.recv()
        print(f"Received reply {request}: {message.decode()}")

# Only execute the following code if this script is run as the main program
if __name__ == "__main__":
    # Create a list to store the client processes
    processes = []
    # Spawn two client processes and add them to the list
    for i in range(2):
        process = mp.Process(target=client_process)
        processes.append(process)
        process.start()

    # Wait for all client processes to finish
    for process in processes:
        process.join()