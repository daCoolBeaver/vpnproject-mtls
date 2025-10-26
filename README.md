# VPN Project – QUIC + mTLS Implementation

This project extends the existing VPN setup by adding secure communication using the **QUIC protocol** combined with Mutual TLS (mTLS) authentication.

It is designed to run inside Docker containers and allows encrypted message exchange between a server and client.

---

## 🚀 How to Run

### 1. Start Docker containers
```bash
docker compose up --build

Start the server

docker exec -it server-router bash -lc 'PYTHONPATH=/volumes PYTHONUNBUFFERED=1 PORT=5460 python3 -u /volumes/server/mtls_quic_server.py'


Start the client

docker exec -it client-10.9.0.5 bash -lc 'PYTHONPATH=/volumes PYTHONUNBUFFERED=1 PORT=5460 CLIENT_CERT=/volumes/keys/tls/client/client.crt CLIENT_KEY=/volumes/keys/tls/client/client.key CA_CERT=/volumes/keys/tls/ca/ca.crt python3 -u /volumes/client/mtls_quic_client.py'


Expected output

Server
server got: b'hello'

Client
client got: b'echo:hello'


