import random
from typing import Any
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Client(DatagramProtocol):
    def __init__(self, host, port):
        self.id = host, port
        self.address = None
        self.server = None #'127.0.0.1', 9999
        print("Working on id: ", self.id)

    def choise_peer(self):
        self.address = input("Write host: "), int(input("write port: "))
        reactor.callInThread(self.send_message)

    def startProtocol(self):
        if (self.server):
            self.transport.write("ready".encode('utf-8'), self.server)
            return

        self.choise_peer()

    def datagramReceived(self, datagram: bytes, addr: Any) -> None:
        datagram = datagram.decode('utf-8')

        if addr == self.server:
            print("Chose a client from these\n", datagram)
            self.choise_peer()
            return

        print(addr, ":", datagram)

    def send_message(self, message):
        self.transport.write(input("> ").encode('utf-8'), self.address)

if __name__ == '__main__':
    port = random.randint(1000, 5000)
    reactor.listenUDP(port, Client('127.0.0.1', port))
    reactor.run()