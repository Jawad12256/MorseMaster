'''NETWORKING MANAGER'''
from pyre import Pyre, zhelper 
import zmq
import uuid
import json

class Peer:
    def __init__(self, nickname):
        self.ctx = zmq.Context()
        self.killed = False
        self.chat_pipe = zhelper.zthread_fork(self.ctx, self.chat_task) #zthread for incoming chat messages
        self.nickname = nickname
        self.peerSelection = []
        self.idDictionary = {} 

    def killPeer(self):
        #kill ZMQ context and processes
        self.killed = True
        self.killed = True
        self.n.stop()

    def sendMessage(self, message, peers):
        #set recipient peers
        #write message to pipe
        print(message)
        print(peers)
        self.peerSelection = peers
        self.chat_pipe.send(message.encode('utf-8'))

    def chat_task(self, ctx, pipe):
        self.n = Pyre("CHAT")
        self.n.set_header("NICKNAME",self.nickname)
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
                print('POLL IN')
                message = pipe.recv() #get outbound message from the pipe
                print(f"Sending message: {str(message)}")
                # for peer in self.peerSelection:
                    # peerRef = uuid.UUID(bytes=peer)
                    # self.n.whispers(peerRef, message.decode('utf-8'))
                self.n.shouts("CHAT", message.decode('utf-8'))
            #elif self.n.socket() in items and items[self.n.socket()] == zmq.POLLIN:
            else:
                #RECEIVING MESSAGE
                cmds = self.n.recv()
                senderPeerID = uuid.UUID(bytes=cmds[1])
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
                    #add peer to dictionary
                    headers = json.loads(cmds[3].decode('utf-8'))
                    TCPPort = str(cmds[4].decode('utf-8'))
                    print(f"TCP/PORT: {TCPPort}")
                    self.idDictionary[senderPeerID] = headers['NICKNAME'] #dictionary format - id:nickname
                elif messageType == 'EXIT':
                    #remove peer from dictionary
                    self.idDictionary.pop(senderPeerID)
                    if senderPeerID in self.peerSelection:
                        self.peerSelection.remove(senderPeerID)
                print(f"PEER ID: {str(senderPeerID)}")
                print(f"MESSAGE TYPE: {messageType}")
                print('---------------------------------------------')
    
    def getUpdatedPeers(self):
        #getter method for list of id dictionary values (nicknames)
        return self.idDictionary.values()

    def getNicknameDict(self):
        #getter method for reversed key-value version of idDictionary
        return {v:k for k,v in self.idDictionary.items()}

    def setNickname(self, newNickname):
        #setter method for nickname
        self.nickname = newNickname
        self.n.stop()
        self.n = Pyre("CHAT")
        self.n.set_header("NICKNAME",self.nickname)
        self.n.join("CHAT")
        self.n.start()