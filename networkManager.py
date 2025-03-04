'''NETWORKING MANAGER'''
from pyre import Pyre, zhelper 
import zmq
import uuid
import json

class Peer:
    def __init__(self, nickname):
        self.ctx = zmq.Context()
        self.killed = False
        self.nickname = nickname
        self.chat_pipe = zhelper.zthread_fork(self.ctx, self.chat_task) #zthread for incoming chat messages
        self.peerSelection = []
        self.idDictionary = {}
        self.inbox = [] #list of (nickname, message) tuples for peer to store its inbound messages

    def killPeer(self):
        #kill ZMQ context and processes
        self.killed = True
        self.killed = True
        self.n.stop()

    def sendMessage(self, message, peers):
        #set recipient peers
        #write message to pipe
        self.peerSelection = peers
        self.chat_pipe.send(message.encode('utf-8'))

    def chat_task(self, ctx, pipe):
        self.n = Pyre("CHAT")
        self.n.set_header("NICKNAME",self.nickname)
        self.n.join("CHAT")
        self.n.start()

        #poller to manage communications with peers
        self.poller = zmq.Poller()
        self.poller.register(pipe, zmq.POLLIN) #for outbound messages
        self.poller.register(self.n.socket(), zmq.POLLIN) #for inbound messages
        while not self.killed:
            items = dict(self.poller.poll(500))
            if pipe in items and items[pipe] == zmq.POLLIN:
                #SENDING MESSAGE
                message = pipe.recv() #get outbound message from the pipe
                for peer in self.peerSelection:
                    self.n.whispers(peer, message.decode('utf-8'))
                # self.n.shouts("CHAT", message.decode('utf-8'))
            elif self.n.socket() in items and items[self.n.socket()] == zmq.POLLIN:
                #RECEIVING MESSAGE
                cmds = self.n.recv()
                senderPeerID = uuid.UUID(bytes=cmds[1])
                messageType = str(cmds[0].decode('utf-8'))
                if messageType == 'SHOUT':
                    #decode message contents if it is a shout message
                    messageContent = str(cmds[4])
                    self.inbox.append((self.idDictionary[senderPeerID],messageContent))
                elif messageType  == 'WHISPER':
                    #decode message contents if it is a whisper message
                    messageContent = str(cmds[3])
                    self.inbox.append((self.idDictionary[senderPeerID],messageContent))
                elif messageType == 'ENTER':
                    #decode TCP and port if it is a new peer entering
                    #add peer to dictionary
                    headers = json.loads(cmds[3].decode('utf-8'))
                    self.idDictionary[senderPeerID] = headers['NICKNAME'] #dictionary format - id:nickname
                elif messageType == 'EXIT':
                    #remove peer from dictionary
                    self.idDictionary.pop(senderPeerID)
                    if senderPeerID in self.peerSelection:
                        self.peerSelection.remove(senderPeerID)
    
    def getUpdatedPeers(self):
        #getter method for list of id dictionary values (nicknames)
        return self.idDictionary.values()

    def getNicknameDict(self):
        #getter method for reversed key-value version of idDictionary
        return {v:k for k,v in self.idDictionary.items()}
    
    def getInbox(self):
        #getter method for updated message inbox
        return self.inbox