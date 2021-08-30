import asyncio
import websockets
from json import dumps

loop = asyncio.new_event_loop()

async def send_message(obj: {}, url: ''):
    ws = await websockets.connect(url)
    try:
        message = dumps(obj)
        await ws.send(message)
    finally:
        await ws.close()