import asyncio
import websockets
import json


class Server:
    clients = {}

    async def register(self, ws):
        if (ws.path not in self.clients):
            self.clients[ws.path] = set()
        self.clients[ws.path].add(ws)

    async def unregister(self, ws):
        self.clients[ws.path].remove(ws)

    async def send_to_clients(self, message, path, exclude_id = None):
        for client in self.clients[path]:
            if (exclude_id != None and hasattr(client, 'reg_id') and client.reg_id != message['exclude_id']):
                await client.send(json.dumps(message))
            elif (exclude_id == None):
                await client.send(message)

    async def send_to_list_clients(self, message, path, list_idx = None):
        for client in self.clients[path]:
            if (hasattr(client, 'reg_id') and client.reg_id in list_idx):
                await client.send(json.dumps(message))

    async def send_to_specific_client(self, message, path, reg_id):
        for client in self.clients[path]:
            if (hasattr(client, 'reg_id') and client.reg_id == reg_id):
                await client.send(message)

    async def distribute(self, ws):
        while True:
            message = await ws.recv()
            try:
                message_dict = json.loads(message)
                if message_dict['type'] == 'reg':
                    for client in self.clients[ws.path]:
                        if (client == ws):
                            client.reg_id = message_dict['id']
                            break
                elif message_dict['type'] == 'exclude':
                    await self.send_to_clients(message_dict, ws.path, message_dict['exclude_id'])
                elif message_dict['type'] == 'to':
                    for client in self.clients[ws.path]:
                        if (hasattr(client, 'reg_id') and client.reg_id == message_dict['to_id']):
                            await self.send_to_specific_client(message_dict, ws.path,
                                                                    message_dict['to_id'])
                            break
                elif message_dict['type'] == 'list':
                    await self.send_to_list_clients(message_dict, ws.path, message_dict['list_idx'])
                else:
                    await self.send_to_clients(message, ws.path)
            except json.JSONDecodeError:
                await self.send_to_clients(message, ws.path)

            except TypeError:
                await self.send_to_clients(message, ws.path)

    async def ws_handler(self, ws, uri):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)


server = Server()
start_server = websockets.serve(server.ws_handler, '192.168.137.100', 8765)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
