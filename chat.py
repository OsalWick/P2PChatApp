import socket
import threading
import sys
from colorama import init, Fore, Style
import time

# Initialize colorama
init()

class ChatApp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.connected = False

    def start_chat(self):
        choice = input("Do you want to (1) host or (2) connect? Enter 1 or 2: ")
        
        if choice == "1":
            self.is_host = True
            self.host_chat()
        else:
            self.connect_to_host()

    def host_chat(self):
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"\nYour IP address is: {local_ip}")
        
        # Bind to port 12345
        self.sock.bind(('', 12345))
        self.sock.listen(1)
        print("Waiting for someone to connect...")
        
        # Accept connection
        self.connection, self.client_address = self.sock.accept()
        self.connected = True
        print(f"\nConnected to {self.client_address[0]}")
        
        # Start message threads
        self.start_message_threads()

    def connect_to_host(self):
        host_ip = input("\nEnter the IP address to connect to: ")
        try:
            self.sock.connect((host_ip, 12345))
            self.connection = self.sock
            self.connected = True
            print(f"\nConnected to {host_ip}")
            
            # Start message threads
            self.start_message_threads()
        except:
            print("Could not connect to the host. Make sure the IP is correct and the host is running.")
            sys.exit()

    def start_message_threads(self):
        # Start receiving thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Start sending thread
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.daemon = True
        send_thread.start()
        
        # Keep main thread alive
        while self.connected:
            time.sleep(1)

    def receive_messages(self):
        while self.connected:
            try:
                if self.is_host:
                    data = self.connection.recv(1024)
                else:
                    data = self.sock.recv(1024)
                
                if not data:
                    break
                    
                # Print received message in green
                print(f"\r{Fore.GREEN}{data.decode()}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}You: {Style.RESET_ALL}", end='', flush=True)
                
            except:
                self.connected = False
                break
        
        print("\nConnection closed.")
        sys.exit()

    def send_messages(self):
        while self.connected:
            try:
                message = input(f"{Fore.BLUE}You: {Style.RESET_ALL}")
                if not message:
                    continue
                    
                if self.is_host:
                    self.connection.send(message.encode())
                else:
                    self.sock.send(message.encode())
                    
            except:
                self.connected = False
                break

if __name__ == "__main__":
    print("Osal & Talia's Personal Chat Space ")
    print("==========================")
    
    chat = ChatApp()
    chat.start_chat()