# dChat — Terminal-Based P2P Mini-Blockchain Chat

O **dChat** é um experimento educativo de mensageria descentralizada que combina:
- uma **rede P2P simples**,  
- um **chat via terminal**,  
- e uma **mini-blockchain local** usada como log encadeado de mensagens.

Não há criptografia, consenso ou assinaturas ainda — o projeto é voltado para estudo de arquitetura distribuída mínima.

---

## Objetivos do Projeto

- Demonstrar comunicação descentralizada sem servidor central.
- Explorar propagação P2P via broadcast.
- Registrar mensagens em estrutura encadeada por hash.
- Criar base para implementações futuras mais avançadas.

---

## Como Executar

```bash
git clone https://github.com/Iago1221/dChat---A-Terminal-Based-P2P-Blockchain-Chat.git
cd dChat---A-Terminal-Based-P2P-Blockchain-Chat

python3 main.py
```
Para simular múltiplos nós, abra várias janelas no terminal e execute.

## Estrutura do Projeto

```
├── main.py
├── models/
├── p2p/
└── services/
```


---

## 4. Arquitetura Geral

O sistema é dividido em três camadas principais:

- **Interface de Chat**  
  Captura a entrada do usuário e exibe mensagens recebidas.

- **Camada P2P**  
  Responsável por:
  - iniciar o nó,
  - enviar e receber mensagens por broadcast,
  - gerenciar peers conectados,
  - repassar mensagens ao serviço de chat.

- **Mini-Blockchain**  
  Registro local e ordenado das mensagens:
  - hashing SHA-256,
  - encadeamento por hash anterior,
  - imutabilidade estrutural,
  - verificação básica da integridade da cadeia.

---

## 5. Fluxo da Mensagem

1. O usuário digita uma mensagem no terminal.  
2. O serviço de chat empacota os dados (usuário, timestamp, texto).  
3. O nó P2P transmite o payload para todos os peers.  
4. Cada peer:
   - recebe a mensagem,
   - adiciona um bloco local registrando aquele conteúdo,
   - exibe no chat.

---

## 6. Componentes

### 6.1. Chat Service
- Recebe entrada do usuário.
- Formata mensagens.
- Envia ao P2P.
- Exibe mensagens recebidas.

### 6.2. P2P Node
- Descobre nós na rede.
- Transmite e recebe mensagens.
- Encaminha mensagens decodificadas ao chat.

### 6.3. Mini-Blockchain
- `Block`: contém idex, timestamp, mensagem, hash e hash anterior.
- `Blockchain`: valida encadeamento e registra cada nova mensagem como bloco.

---

## 7. Exemplo de Estrutura de Bloco

```json
{
  "index": 42,
  "timestamp": "2025-12-03T11:30:20",
  "message": {
    "content": "mensagem...",
    "identity": {
        "id": 5,
        "username": "Usuário"
    }
  },
  "previous_hash": "abc123...",
  "hash": "9f0c1..."
}
```

## Limitações Conhecidas 
- Não há criptografia.
- Não há consenso distribuído real.
- Cada nó mantem sua própria cópia local e divergências são possíveis.
- Não implementa prevenção de duplicatas
- Comunicação somente via broadcast local.

## Roadmap
- Criptografia de ponta a ponta.
- Assinatura digital das mensagens.
- Deteção de duplicatas.
- Interface gráfica opcional.
- Adoção de protocolos de distribução mais robustos.

## Aviso Importante
Este software é experimental, didático e não adequado para comnuicação real.
Não há segurança, anonimato ou sigilo de dados.
Utilize apenas para fins de estudos