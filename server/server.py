import sys
from asyncio import get_event_loop
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLS_SERVER

import websockets


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"<- {name}")

    greeting = f"Hello {name}!"
    await websocket.send(greeting)

    while True:
        command = input(f"What should {name} do? ")

        await websocket.send(command)
        print(f"-> {command}")
        if command == 'Exit':
            sys.exit(0)


ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
localhost_pem = Path(__file__).with_name("local.pem")
ssl_context.load_cert_chain(localhost_pem)

start_server = websockets.serve(
    hello, "localhost", 8765, ssl=ssl_context
)

get_event_loop().run_until_complete(start_server)
get_event_loop().run_forever()
