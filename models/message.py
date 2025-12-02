from models.identity import Identity


class Message:
    def __init__(self, identity: Identity, content):
        self.identity = identity
        self.content = content

    def _serialize(self):
        return {
            "content": self.content,
            "identity": self.identity._serialize()
        }