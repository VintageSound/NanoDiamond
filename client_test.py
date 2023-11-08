import socket
import json

server_ip = "132.72.13.187"
server_port = 50001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    # Get an array of integers from the user
    input_data = input("Enter an array of floats (comma-separated): ")
    if input_data.lower() == 'exit':
        break

    # Convert the input string into a Python list of integers
    float_array = [float(x) for x in input_data.split(',')]

    # Serialize the list as a JSON string before sending
    data_to_send = json.dumps(float_array)

    # Send the data to the server
    client_socket.send(data_to_send.encode('utf-8'))

client_socket.close()
