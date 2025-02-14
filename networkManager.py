'''NETWORKING MANAGER'''
import socket
from time import sleep

class TCPServer():
    def __init__(self, name):
        #initialise host and port
        self.host = '127.0.0.1'
        self.port = 8080
        self.name = name
        self.maxclients = 8
        self.nameRequestWait = 1.0
        self.connections = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.bind((self.host, self.port))
        self.establishClients()
    
    def establishClients(self):
        #establish clients for the TCP server
        self.connections = {}
        self.sock.listen(8)
        print('Establishing clients') 
        for i in range(self.maxclients):
            #establish socket connection object and get client name
            #pass name to create TCPClient object
            #store TCPClient object against socket connection object in dictionary
            #dictionary - TCPClient(clientName):conn
            conn = self.sock.accept() 
            self.sendNameRequestToClient(conn)
            sleep(self.nameRequestWait)
            try:
                clientName = self.getDataFromClient(conn)
            except:
                clientName = f"Client {i}"
            self.connections[TCPClient(clientName)] = conn
            print(f"Connected with {clientName}")
    
    def getClients(self):
        #getter method for connections dictionary
        return self.connections

    def getDataFromClient(self, conn):
        #takes in a socket connection object as a parameter and gets data if it exists
        receivedData = conn.recv(1024).decode()
        if receivedData:
            return receivedData
    
    def sendDataToClient(self, conn, data):
        #takes in a socket connection object as a parameter and data to send, and sends it to that client
        conn.send(data.encode())

    def sendNameRequestToClient(self, conn):
        #takes in a socket connection object as a parameter and sends a name request token as data to that client
        nameRequestToken = '\\NAMEREQUEST'
        conn.send(nameRequestToken.encode())
        

class TCPClient():
    def __init__(self, name):
        #initialise host and port
        self.host = '127.0.0.1'
        self.port = 8080
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.connect((self.host, self.port))

    def getName(self):
        return self.name

    def sendDataToServer(self, data):
        #takes in data as a parameter, and encodes and sends it to the server
        self.sock.send(data.encode())

    def sendNameToServer(self):
        #encodes and sends the client name to the server
        self.sock.send(self.name.encode())

    def getDataFromServer(self):
        #get data sent from the server
        #call the appropriate method if the data received is a name request token
        data = self.sock.recv(1024).decode()
        if data == '\\NAMEREQUEST':
            self.sendNameToServer()
            return None
        return data

