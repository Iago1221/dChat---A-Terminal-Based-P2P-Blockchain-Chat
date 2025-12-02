import os
from models.blockchain import Blockchain
from models.identity import Identity
from models.message import Message
import datetime
from p2p.p2p_node import P2PNode

class Chat:
    def __init__(self, identity: Identity, p2p: P2PNode, initialize_chain = True):
        self.identity = identity
        self.chain = Blockchain(initialize_chain)
        self.p2p = p2p
        p2p.chat = self

    def render(self):
        print("\033c", end="")

        print(f"host: {self.p2p.port}")
        print("===== CHAT =====\n")

        for block in self.chain.chain:
            msg = block.message
            ts = datetime.datetime.fromtimestamp(block.timestamp).strftime("%H:%M")
            print(f"[{msg.identity.username} @ {ts}] {msg.content}")

        print("\n----------------------------")
        print("> ", end="", flush=True)

    def send_local_message(self, content):
        msg = Message(self.identity, content)
        block = self.chain.add_block(msg)
        self.p2p.broadcast_block(block)
        self.render()

    def on_new_remote_block(self, block):
        self.chain.chain.append(block)
        self.render()

    def render_blockchain(self):
        print("\n===== BLockchain =====\n")

        for block in self.chain.chain:
            print(block._serialize())
            print("\n----------------------------")

        print("====== FIM ======\n")

    def stop(self):
        self.render_blockchain()
        from twisted.internet import reactor
        reactor.stop()