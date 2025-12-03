import sys
from threading import Thread
from twisted.internet import reactor, stdio
from models.identity import Identity
from p2p.p2p_node import P2PNode
from services.chat import Chat
import random

def input_thread(chat):
    while True:
        line = sys.stdin.readline().strip()

        if line == '/exit':
            reactor.callFromThread(chat.stop)
            return

        reactor.callFromThread(chat.send_local_message, line)

def start_input(chat):
    Thread(target=input_thread, args=(chat,), daemon=True).start()

def definir_identidade():
    identity = Identity()
    identity.set_username(input("Seu usuário: "))
    return identity

def conectar_chat():
    identity = definir_identidade()
    sys_port = random.randint(10000, 50000)

    p2p = P2PNode(None, sys_port)
    chat = Chat(identity, p2p, False)

    print(f"Conectado na porta {sys_port}")
    reactor.listenUDP(sys_port, p2p)

    peer_host = input("Peer host: ")
    peer_port = int(input("Peer port: "))
    p2p.add_peer(peer_host, peer_port)

    p2p.request_chain()

    start_input(chat)

    chat.render()
    reactor.run()

def iniciar_chat():
    identity = definir_identidade()

    sys_port = random.randint(10000, 50000)

    p2p = P2PNode(None, sys_port)
    chat = Chat(identity, p2p)

    print(f"Conectado na porta {sys_port}")
    reactor.listenUDP(sys_port, p2p)

    start_input(chat)

    chat.render()
    reactor.run()

def menu():
    print('--------------------------------')
    print('- 1 - Iniciar novo chat        -')
    print('- 2 - Entrar em chat existente -')
    print('--------------------------------')
    command = input('> ')
    return int(command) if command.isdigit() else 3

def main():
    command = menu()

    match command:
        case 1:
            iniciar_chat()
        case 2:
            conectar_chat()
        case _:
            print("Entrada inválida, saindo...")

if __name__ == "__main__":
    main()
