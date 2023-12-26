# configure the connection
import socket
import json
import threading

from PulseSequencer.Data.measurementType import measurementType

server_ip = "132.72.13.187"
server_port = 50001

# Function to handle the client connection
def handle_client_connection(client_socket, client_address):
    global received_data
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Parse the received JSON string into a Python list
        received_data = json.loads(data)
        print(f"Received data from {client_address}: {received_data}")

        # Signal that data is available
        data_available_event.set()

    client_socket.close()
    print(f"Connection from {client_address} closed")

# Variable to hold received data
received_data = None

# Variable to hold the client socket
client_socket = None

# Event to signal that data is available
data_available_event = threading.Event()

# Create a server socket and bind it to a specific IP and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print(f"Listening on {server_ip}:{server_port}")

# Lock to protect access to the client_socket variable
client_socket_lock = threading.Lock()

def connect_client():
    global client_socket
    try:
        while True:
            try:
                # Accept a client connection
                with client_socket_lock:
                    client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")

                # Create a thread to handle the client connection
                client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
                client_thread.start()
            except socket.timeout:
                print("No client connection within the timeout period.")
            except KeyboardInterrupt:
                print("Server stopped by the user.")
                break
    finally:
        server_socket.close()

def receive_data():
    global received_data
    global client_socket
    while True:
        try:
            with client_socket_lock:
                data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Parse the received JSON string into a Python list
            received_data = json.loads(data)
            print(f"Received data: {received_data}")

            # Signal that data is available
            data_available_event.set()

        except (ConnectionResetError, ConnectionAbortedError):
            print("Client disconnected.")
            with client_socket_lock:
                client_socket = None  # Reset the client_socket
            break

    if client_socket is not None:
        with client_socket_lock:
            client_socket.close()
# configure the Pulse Blaster settings

try:
    # Load spinapi.py in current folder
    from spinapi import *

except:
    # Load spinapi.py in the folder one level up
    import sys
    sys.path.append('../../')
    from spinapi import *

clock_freq = 500

def pause():
    input("Press enter to continue...")


def detect_boards():
    global numBoards

    numBoards = pb_count_boards()

    if numBoards <= 0:
        print("No Boards were detected in your system. Verify that the board "
              "is firmly secured in the PCI slot.\n")
        pause()
        exit(-1)


def select_boards():
    while True:
        try:
            choice = int(
                input(f"Found {numBoards} boards in your system. Which board should be used? (0-{numBoards - 1}): "))
            if choice < 0 or choice >= numBoards:
                print("Invalid Board Number (%d)." % choice)
            else:
                pb_select_board(choice)
                print("Board %d selected." % choice)
                break;
        except ValueError:
            print("Incorrect input. Please enter a valid board number.")


def input_clock():
    global clock_freq
    while True:
        try:
            clock_freq = float(input("\nPlease enter internal clock frequency (MHz): "))
            break  # Break out of the loop if a valid number is entered
        except ValueError:
            print("Incorrect input. Please enter a valid clock frequency.")


# Uncommenting the line below will generate a debug log in your current
# directory that can help debug any problems that you may be experiencing
# pb_set_debug(1)


#print("Copyright (c) 2023 SpinCore Technologies, Inc.\n")

#print("Using SpinAPI Library version %s" % pb_get_version())

# If there is more than one board in the system, have the user specify.
detect_boards()

if numBoards > 1:
    select_boards()

if pb_init() != 0:
    print("Error initializing board: %s" % pb_get_error())
    pause()
    exit(-1)

# User input clock
# input_clock()
clock_freq = 500

print("\nClock frequency: %1fMHz\n" % clock_freq)


# Tell driver what clock frequency the board uses
pb_core_clock(clock_freq)

def programm_pb_sequence():
    while True:
        # Wait for data to be available
        data_available_event.wait()
        print('data available')
        # Clear the event
        data_available_event.clear()

        # Now you can use the received_data in this thread
        if received_data is not None:
            start_pump = float(received_data[0])
            width_pump = float(received_data[1])
            start_mw = float(received_data[2])
            width_mw = float(received_data[3])
            start_image = float(received_data[4])
            width_image = float(received_data[5])
            mw_open = received_data[6]
            tau = width_mw
            half_pi_duration = float(0.16)
            pi_duration = 2 * half_pi_duration

            if mw_open:
                # program Rabi sequence
                pb_start_programming(PULSE_PROGRAM)
                start = pb_inst_pbonly(0, WAIT, 0, 0.3 * us)  # wait for 300ns from the end of the pump pulse to the start of the MW
                pb_inst_pbonly(ON | 0xE, CONTINUE, 0, width_mw * us)
                pb_inst_pbonly(0, BRANCH, start, (start_image-start_pump) * us)
                pb_stop_programming()  # Finished sending instructions
                pb_reset()
                pb_start()  # Trigger the pulse program
                print("Rabi sequence started")

                # pb_start_programming(PULSE_PROGRAM)
                # start = pb_inst_pbonly(0, WAIT, 0, 0.3 * us)  # wait for 300ns from the end of the pump pulse to the start of the MW
                # pb_inst_pbonly(ON | 0xE, CONTINUE, 0, half_pi_duration * us)
                # pb_inst_pbonly(0, CONTINUE, 0, tau * us)
                # pb_inst_pbonly(ON | 0xE, CONTINUE, 0, half_pi_duration * us)
                # pb_inst_pbonly(0, BRANCH, start, (start_image - start_pump) * us)
                # pb_stop_programming()  # Finished sending instructions
                # pb_reset()
                # pb_start()  # Trigger the pulse program
                # print("Ramsey sequence started")
            else:
                # ODMR - leave MW constantly on
                pb_start_programming(PULSE_PROGRAM)
                start = pb_inst_pbonly(ON | 0xE, CONTINUE, 0, 5 * us)
                pb_inst_pbonly(ON | 0xE, BRANCH, start, 5 * us)
                pb_stop_programming()  # Finished sending instructions
                pb_reset()
                pb_start()  # Trigger the pulse program
                print("constantly on")
    pb_close()
    pause()

# create threads

get_data = threading.Thread(target=receive_data, name="get_data")
programm_pb = threading.Thread(target=programm_pb_sequence, name="programm_pb_sequence")
connect_client = threading.Thread(target=connect_client, name='connect_client')

connect_client.start()
get_data.start()
programm_pb.start()
