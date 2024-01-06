import asyncio
import websockets
from aiohttp import web

async def handle_send_message(request):
    message = request.query.get('message', 'Hello, World!')
    await broadcast_message(message)
    return web.Response(text=f'Message "{message}" broadcasted to all clients')

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Add the new WebSocket connection to the list of connected clients
    connected_clients.add(ws)

    async for msg in ws:
        # Handle incoming WebSocket messages (if needed)
        pass

    # Remove the WebSocket connection when it is closed
    connected_clients.remove(ws)
    print("WebSocket connection closed")

    return ws

async def broadcast_message(message):
    # Broadcast the message to all connected clients
    for client in connected_clients:
        await client.send_str(message)

async def handle_root(request):
    # Serve the static HTML file at the root path
    return web.FileResponse('./index.html')

app = web.Application()
app.router.add_get('/sendMessage', handle_send_message)
app.router.add_get('/ws', handle_websocket)
app.router.add_get('/', handle_root)

connected_clients = set()

if __name__ == '__main__':
    web.run_app(app, port=8080, host='localhost')
    # web.run_app(app, port=85, host='0.0.0.0')
