import json
from twisted.internet.protocol import DatagramProtocol
from models.block import Block

class P2PNode(DatagramProtocol):
    def __init__(self, chat_service, port):
        self.chat = chat_service
        self.peers = []
        self.port = port

    def request_chain(self):
        payload = json.dumps({
            "type": "sync"
        }).encode()

        self.transport.write(payload, self.peers[-1])

    def sync_peers(self, addr):
        payload = json.dumps({
            "type": "peers",
            "peers": self.peers
        }).encode()

        self.transport.write(payload, addr)

    def sync_chain(self, addr):
        for block in self.chat.chain.chain:
            payload = json.dumps({
                "type": "block",
                "data": block._serialize()
            }).encode()

            self.transport.write(payload, addr)

    def add_peer(self, host, port):
        self.peers.append((host, port))

    def datagramReceived(self, data, addr):
        try:
            print(addr)
            payload = json.loads(data.decode())
        except:
            print("Recebido não-JSON:", data)
            return

        if payload["type"] == "block":
            block = Block._construct(payload["data"])
            from twisted.internet import reactor
            reactor.callLater(0, self.chat.on_new_remote_block, block)
        elif payload["type"] == "sync":
            self.sync_peers(addr)
            self.sync_chain(addr)
            self.broadcast_new_peer(addr)
            self.add_peer(addr[0], addr[1])
        elif payload["type"] == "new_peer":
            self.add_peer(payload["host"], payload["port"])
        elif payload["type"] == "peers":
            self.received_peers(payload["peers"])

    def broadcast_block(self, block):
        payload = json.dumps({
            "type": "block",
            "data": block._serialize()
        }).encode()

        for p in self.peers:
            self.transport.write(payload, p)

    def received_peers(self, peers):
        for p in peers:
            self.add_peer(p[0], p[1])

    def broadcast_new_peer(self, addr):
        payload = json.dumps({
            "type": "new_peer",
            "host": addr[0],
            "port": addr[1]
        }).encode()

        for p in self.peers:
            self.transport.write(payload, p)