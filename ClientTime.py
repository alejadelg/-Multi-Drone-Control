import socket
import time
import datetime

def log_time(action):
    """Logs the time with microseconds and returns the timestamp"""
    timestamp = time.time()  # Get the time in seconds including microseconds
    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Trim to milliseconds
    print(f"[SYNC] {action} - Time: {formatted_time}")
    return timestamp

def sync_manual(client_socket):
    """Manual synchronization between GCS and each client"""
    print("Starting manual synchronization with client...")

    # Send initial timestamp from host (GCS)
    send_time = log_time("Timestamp sent from GCS")
    client_socket.send(str(send_time).encode())

    # Receive timestamp from client (drone)
    drone_sync_time = float(client_socket.recv(1024).decode())
    log_time(f"Timestamp received from drone: {drone_sync_time}")

    # Calculate clock offset
    sync_offset = drone_sync_time - send_time
    print(f"Estimated clock offset between GCS and drone: {sync_offset:.6f} seconds\n")

def start_host(host, port):
    """TCP server that handles drone connections and time synchronization"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 clients
    print(f"Host server running on {host}:{port}")

    clients = []  # List of connected clients
    
    while len(clients) < 5:
        conn, addr = server_socket.accept()  # Wait for connection
        print(f"Client connected from {addr}")
        clients.append(conn)
        print(f"Total connected clients: {len(clients)}")

        # Perform manual time synchronization with the client
        sync_manual(conn)

    print("All clients synchronized. Ready to send commands.")

    # Send commands to all clients and log user input time
    while True:
        input_time = log_time("User entered command")  # Capture input time
        command = input("Enter command for drones (e.g., takeoff, land): ")
        send_time = log_time("Command sent to clients")  # Capture send time

        if command.lower() == "exit":
            break

        for client in clients:
            try:
                client.sendall(command.encode())
            except Exception as e:
                print(f"Error sending to client: {e}")
                clients.remove(client)

        # Measure latency from user input to sending to drones
        print(f"Latency from user input to sending: {send_time - input_time:.6f} seconds\n")

    # Close connections
    for client in clients:
        client.close()
    server_socket.close()

# Start the server
host_ip = "117.16.154.115"  # Host IP
port = 8080  # Connection port
start_host(host_ip, port)
