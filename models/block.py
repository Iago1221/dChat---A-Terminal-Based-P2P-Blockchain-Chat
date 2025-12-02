import hashlib
import json
import time

from models.identity import Identity
from models.message import Message


class Block:
    def __init__(self, index, message: Message, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.message = message
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "message": self.message._serialize(),
            "previous_hash": self.previous_hash
        }).encode()

        return hashlib.sha256(block_string).hexdigest()

    def _serialize(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "message": self.message._serialize(),
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def _construct(data):
        idt = Identity()
        idt.id = data['message']['identity']['id']
        idt.set_username(data['message']['identity']['username'])
        msg = Message(idt, data['message']['content'])

        b = Block(
            data['index'],
            msg,
            data['previous_hash']
        )

        b.timestamp = data['timestamp']
        b.hash = data['hash']
        return b