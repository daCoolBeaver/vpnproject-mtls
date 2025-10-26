# /volumes/client/mtls_quic_client.py
import os
import ssl
import asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import connect

# Paths and defaults (match your container mount)
CA_CERT     = os.getenv("CA_CERT", "/volumes/keys/tls/ca/ca.crt")
CLIENT_CERT = os.getenv("CLIENT_CERT", "/volumes/keys/tls/client/client.crt")
CLIENT_KEY  = os.getenv("CLIENT_KEY", "/volumes/keys/tls/client/client.key")

# Talk to the Docker service name of the server
HOST = os.getenv("HOST", "server-router")

# Use 4444 by default to avoid port conflicts you saw on 4433
PORT = int(os.getenv("PORT", "4444"))

async def main():
    cfg = QuicConfiguration(is_client=True, alpn_protocols=["hq-29"])
    cfg.load_cert_chain(CLIENT_CERT, CLIENT_KEY)
    cfg.verify_mode = ssl.CERT_REQUIRED
    cfg.load_verify_locations(CA_CERT)

    # Match the CN/SAN on your server certificate
    cfg.server_name = "vpn.local"

    print(f"client connecting to {HOST}:{PORT}")
    async with connect(HOST, PORT, configuration=cfg) as conn:
        reader, writer = await conn.create_stream()
        payload = b"hello"
        print("client sending:", payload)
        writer.write(payload)
        await writer.drain()
        data = await reader.read(1024)
        print("client got:", data)

if __name__ == "__main__":
    asyncio.run(main())

