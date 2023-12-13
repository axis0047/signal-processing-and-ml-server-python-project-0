import socket
from scipy import signal
import numpy as np

import requests

import math

ws_server_url = 'http://155.65.100.1'
headers = {'Content-Type': 'application/json'}

def udp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific address and port
    server_address = ('0.0.0.0', 5555)  # Listen on all available interfaces
    server_socket.bind(server_address)

    print('UDP server is listening on {}:{}'.format(*server_address))

    try:
        while True:
            # Receive data and address from client
            data, client_address = server_socket.recvfrom(1024)

            # Reconstruct NumPy array from bytes
            reconstructed_array = np.frombuffer(data, dtype=np.float32)

            # Process the reconstructed array
            #fake processing process
            array_sum = np.sum(reconstructed_array)
            
            decision_digit = math.floor(array_sum % 16)
            
            if(decision_digit < 8):
                
                data = {
                        'client_id':2,
                        'desicion':decision_digit
                        }
                
                count = 0
                
                while(count < 10):
                    
                    response = requests.post(ws_server_url, headers=headers, json=data)    

                    if response.status_code == 200:
                        # Request was successful, you can work with the response data
                        data = response.json()  # Assuming the response is in JSON format
                        print(data)
                        break
                    else:
                        # Handle the error
                        print(f"Error: {response.status_code}")
                        print(response.text)  # Print the error response content
                        count = count + 1
            
    finally:
        print("Server stopped.")
        server_socket.close()

if __name__ == '__main__':
    udp_server()