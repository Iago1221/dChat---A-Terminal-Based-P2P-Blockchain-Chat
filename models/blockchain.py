import json

from models.block import Block
from models.identity import Identity
from models.message import Message


class Blockchain:
    def __init__(self, generate = True):
        self.chain = [self.create_genesis_block()] if generate else []

    def create_genesis_block(self):
        return Block(0, Message(Identity('Genesis'), "Genesis Block"), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, message: Message):
        prev = self.get_latest_block()
        new_block = Block(
            prev.index + 1,
            message,
            prev.hash
        )
        self.chain.append(new_block)
        return self.get_latest_block()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            current = self.chain[i]

            if (current.hash != current.calculate_hash()):
                return False

            if (current.previous_hash != prev.hash):
                return False

        return True

    def resume(self):
        for block in self.chain:
            yield json.dumps(block._serialize(), indent=4, ensure_ascii=False)