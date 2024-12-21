import socket
import threading
import sys
from colorama import init, Fore, Style
import time
import os

# Initialize colorama
init()

class ChatApp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.connected = False
        self.username = ""
        self.peer_username = "CONNECTED USER"

    def start_chat(self):
        self.username = input("Please enter your name: ")
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
        
        # Exchange usernames
        self.connection.send(self.username.encode())
        self.peer_username = self.connection.recv(1024).decode()
        print(f"\nConnected to {self.client_address[0]} ({self.peer_username})")
        
        # Start message threads
        self.start_message_threads()

    def connect_to_host(self):
        host_ip = input("\nEnter the IP address to connect to: ")
        try:
            self.sock.connect((host_ip, 12345))
            self.connection = self.sock
            self.connected = True
            
            # Exchange usernames
            self.peer_username = self.connection.recv(1024).decode()
            self.connection.send(self.username.encode())
            print(f"\nConnected to {host_ip} ({self.peer_username})")
            
            # Start message threads
            self.start_message_threads()
        except:
            print("Could not connect to the host. Make sure the IP is correct and the host is running.")
            sys.exit()

    def start_message_threads(self):
        # Clear screen before starting chat
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nChat started! You are chatting as {self.username} with {self.peer_username}")
        
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
                    
                # Print received message with peer's username
                print(f"\r{Fore.GREEN}{self.peer_username}: {data.decode()}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}{self.username}: {Style.RESET_ALL}", end='', flush=True)
                
            except:
                self.connected = False
                break
        
        print("\nConnection closed.")
        sys.exit()

    def send_messages(self):
        while self.connected:
            try:
                message = input(f"{Fore.BLUE}{self.username}: {Style.RESET_ALL}")
                if not message:
                    continue
                    
                if self.is_host:
                    self.connection.send(message.encode())
                else:
                    self.sock.send(message.encode())
                    
            except:
                self.connected = False
                break

    @staticmethod
    def print_title():
        print("""   ____            _ _        _____ _           _     _____                        
             / ____| |         | |   |  __ \\                       
            | |    | |__   __ _| |_  | |__) |___   ___  _ __ ___   
            | |    | '_ \\ / _` | __| |  _  // _ \\ / _ \\| '_ ` _ \\  
             \\ | |____| | | | (_| | |_  | | \\ \\ (_) | (_) | | | | | | 
              \\_____|_| |_|\\__,_|\\__| |_|  \\_\\___/ \\___/|_| |_| |_| 
        """)

if __name__ == "__main__":
    
    
    chat = ChatApp()
    ChatApp.print_title()
    chat.start_chat()