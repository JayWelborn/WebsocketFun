import asyncio
import sys
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLS_CLIENT

import websockets

ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
localhost_pem = Path(__file__).with_name("local.pem")
ssl_context.load_verify_locations(localhost_pem)


def hello():
    print("Hello Websockets")


def parrot():
    print("Polly want a cracker?")


def exit_client():
    print("Exiting...")
    sys.exit()


commands = {
    'Hello': hello,
    'Parrot': parrot,
    'Exit': exit_client
}


async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"-> {name}")

        greeting = await websocket.recv()
        print(f"<- {greeting}")

        while True:
            command = await websocket.recv()

            try:
                commands[command]()
            except KeyError:
                print(f"{command} is an unknown command.")


asyncio.get_event_loop().run_until_complete(hello())
