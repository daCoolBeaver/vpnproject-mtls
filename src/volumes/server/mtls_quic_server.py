import os
import ssl
import asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import serve

CA_CERT     = os.getenv("CA_CERT", "/volumes/keys/tls/ca/ca.crt")
SERVER_CERT = os.getenv("SERVER_CERT", "/volumes/keys/tls/server/server.crt")
SERVER_KEY  = os.getenv("SERVER_KEY", "/volumes/keys/tls/server/server.key")
PORT        = int(os.getenv("PORT", "5454"))

async def handle_stream(reader, writer):
    print("stream opened")
    data = await reader.read(1024)
    if data:
        print("server got:", data)
        writer.write(b"echo:" + data)
        await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("stream closed")

def stream_handler(reader, writer):
    # schedule the coroutine so it actually runs
    asyncio.create_task(handle_stream(reader, writer))

async def main():
    cfg = QuicConfiguration(is_client=False, alpn_protocols=["hq-29"])
    cfg.load_cert_chain(SERVER_CERT, SERVER_KEY)
    cfg.verify_mode = ssl.CERT_REQUIRED
    cfg.load_verify_locations(CA_CERT)

    print(f"QUIC server listening on 0.0.0.0:{PORT}")
    server = await serve("0.0.0.0", PORT, configuration=cfg, stream_handler=stream_handler)

    try:
        await asyncio.Event().wait()  # keep running
    finally:
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
