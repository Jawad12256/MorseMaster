'''NETWORKING MANAGER'''
from pyre import Pyre, zhelper 
import zmq 
import uuid
import json
from time import sleep

class Peer:
    def __init__(self):
        self.ctx = zmq.Context()
        self.killed = False
        self.chat_pipe = zhelper.zthread_fork(self.ctx, self.chat_task) #zthread for incoming chat messages
        self.peerSelection = []
        self.peerDictionary = {}

    def killPeer(self):
        #kill ZMQ context and processes
        self.killed = True
        self.n.stop()

    def sendMessage(self, message, peers):
        #write message to pipe
        self.chat_pipe.send(message.encode('utf-8'))

    def chat_task(self, ctx, pipe):
        self.n = Pyre("CHAT")
        self.n.set_header("NICKNAME","Unknown User")
        self.n.join("CHAT")
        self.n.start()

        #poller to manage peers
        self.poller = zmq.Poller()
        self.poller.register(pipe, zmq.POLLIN)
        self.poller.register(self.n.socket(), zmq.POLLIN)
        while not self.killed:
            items = dict(self.poller.poll(500))
            if pipe in items and items[pipe] == zmq.POLLIN:
                #SENDING MESSAGE
                message = pipe.recv() #get outbound message from the pipe
                print(f"Sending message: {str(message)}")
                self.n.shouts("CHAT", message.decode('utf-8'))
            #elif self.n.socket() in items and items[self.n.socket()] == zmq.POLLIN:
            else:
                #RECEIVING MESSAGE
                cmds = self.n.recv()
                senderPeerID = str(uuid.UUID(bytes=cmds[1]))
                messageType = str(cmds[0].decode('utf-8'))
                if messageType in ('SHOUT','WHISPER'):
                    #decode headers if it is a sent message
                    headers = json.loads(cmds[4].decode('utf-8'))
                    messageContent = str(cmds[6])
                    print('HEADERS:')
                    print(headers)
                    print('MESSAGE CONTENTS:')
                    print(messageContent)
                elif messageType == 'ENTER':
                    #decode TCP and port if it is a new peer entering
                    headers = json.loads(cmds[3].decode('utf-8'))
                    TCPPort = str(cmds[4].decode('utf-8'))
                    print(f"TCP/PORT: {TCPPort}")
                    print(f"HEADERS: {headers}")
                    print(f"NICKNAME: {headers['NICKNAME']}")
                    self.peerDictionary[headers['NICKNAME']] = senderPeerID
                    self.peerSelection = [peerID for peerID in self.peerDictionary.items()] #temporary code to set every peer as a recipient
                print(f"PEER ID: {senderPeerID}")
                print(f"MESSAGE TYPE: {messageType}")
                print('---------------------------------------------')
    
    def getUpdatedPeers(self):
        return self.peerDictionary