# VPN Project – QUIC + mTLS Implementation

This project extends the existing VPN setup by adding secure communication using the **QUIC protocol** combined with Mutual TLS (mTLS) authentication.

It is designed to run inside Docker containers and allows encrypted message exchange between a server and client.

---

## 🚀 How to Run

## 🔐 Certificate Setup (Manual)
Generate CA, Server, and Client certificates manually using OpenSSL:

# 1. Create a Certificate Authority (CA)
openssl genrsa -out keys/tls/ca/ca.key 2048
openssl req -x509 -new -nodes -key keys/tls/ca/ca.key -sha256 -days 365 -out keys/tls/ca/ca.crt -subj "/CN=MyVPN-CA"

# 2. Generate the Server Certificate
openssl genrsa -out keys/tls/server/server.key 2048
openssl req -new -key keys/tls/server/server.key -out keys/tls/server/server.csr -subj "/CN=server-router"
openssl x509 -req -in keys/tls/server/server.csr -CA keys/tls/ca/ca.crt -CAkey keys/tls/ca/ca.key -CAcreateserial -out keys/tls/server/server.crt -days 365 -sha256

# 3. Generate the Client Certificate
openssl genrsa -out keys/tls/client/client.key 2048
openssl req -new -key keys/tls/client/client.key -out keys/tls/client/client.csr -subj "/CN=client"
openssl x509 -req -in keys/tls/client/client.csr -CA keys/tls/ca/ca.crt -CAkey keys/tls/ca/ca.key -CAcreateserial -out keys/tls/client/client.crt -days 365 -sha256

# Directory of each file
src/keys/tls/ca → CA certs
src/keys/tls/server → server.crt, server.key
src/keys/tls/client → client.crt, client.key


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


