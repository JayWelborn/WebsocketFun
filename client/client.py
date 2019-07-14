import asyncio
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLS_CLIENT

import websockets

ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
localhost_pem = Path(__file__).with_name("local.pem")
ssl_context.load_verify_locations(localhost_pem)


async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hello())
