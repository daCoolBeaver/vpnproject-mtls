# VPN Project – QUIC + mTLS Implementation

This project extends the existing VPN setup by adding secure communication using the **QUIC protocol** combined with Mutual TLS (mTLS) authentication.

It is designed to run inside Docker containers and allows encrypted message exchange between a server and client.

---

⚙️ Setup Instructions
1. Clone and build
git clone https://github.com/daCoolBeaver/vpnproject-mtls.git
cd vpnproject-mtls/src
docker compose up -d --build


This will start three containers:

server-router (the QUIC + mTLS server)

client-10.9.0.5 (the mTLS client)

host-192.168.60.7 (internal network host)

2. 🔐 Generate Certificates Manually with OpenSSL

You need to create your own certificates before running the client and server.
Run these commands inside the src/keys/tls folder.

# Create folders if missing
mkdir -p ca server client

# 1️⃣ Create a Certificate Authority (CA)
openssl genrsa -out ca/ca.key 2048
openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days 365 \
    -out ca/ca.crt -subj "/CN=VPN-CA"

# 2️⃣ Generate the Server Certificate
openssl genrsa -out server/server.key 2048
openssl req -new -key server/server.key -out server/server.csr -subj "/CN=server-router"
openssl x509 -req -in server/server.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out server/server.crt -days 365 -sha256

# 3️⃣ Generate the Client Certificate
openssl genrsa -out client/client.key 2048
openssl req -new -key client/client.key -out client/client.csr -subj "/CN=client"
openssl x509 -req -in client/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out client/client.crt -days 365 -sha256


✅ File structure after setup

src/keys/tls/
├── ca/
│   ├── ca.crt
│   └── ca.key
├── server/
│   ├── server.crt
│   └── server.key
└── client/
    ├── client.crt
    └── client.key

3. 🚀 Run the Server and Client

Run the server (in one terminal):

docker exec -it server-router bash -lc \
'PYTHONPATH=/volumes PYTHONUNBUFFERED=1 PORT=5460 \
python3 -u /volumes/server/mtls_quic_server.py'


Run the client (in another terminal):

docker exec -it client-10.9.0.5 bash -lc \
'PYTHONPATH=/volumes PYTHONUNBUFFERED=1 PORT=5460 \
CLIENT_CERT=/volumes/keys/tls/client/client.crt \
CLIENT_KEY=/volumes/keys/tls/client/client.key \
CA_CERT=/volumes/keys/tls/ca/ca.crt \
python3 -u /volumes/client/mtls_quic_client.py'

4. ✅ Expected Output

If everything is working, you should see:

Server terminal:

stream opened
server got: b'hello'


Client terminal:

client sending: b'hello'
client got: b'echo:hello'


This confirms successful QUIC + mTLS communication between the containers.

5. 💡 Notes

hq-29 refers to the Application-Layer Protocol Negotiation (ALPN) identifier used in the QUIC/HTTP3 draft version 29.
It’s not directly tied to mTLS — it just defines the QUIC protocol version.

Certificates are not auto-generated.
They must be created manually using the OpenSSL commands above.

Ensure your .gitignore includes:

src/keys/


to prevent committing private keys or certificates to GitHub.
