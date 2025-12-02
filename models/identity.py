import uuid

class Identity:
    def __init__(self, username=None):
        self.id = str(uuid.uuid4())
        self.username = username

    def set_username(self, username):
        self.username = username

    def _serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }
