from twisted.protocols.basic import LineReceiver

class ChatInput(LineReceiver):
    delimiter = b"\n"

    def __init__(self, chat):
        self.chat = chat

    def lineReceived(self, line):
        msg = line.decode().strip()

        if msg == '/exit':
            self.chat.stop()
            return

        self.chat.send_local_message(msg)