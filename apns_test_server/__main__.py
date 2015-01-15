import asyncio
from handlers import request_handler

# OPTIONS

HOSTNAME = "127.0.0.1"
PORT = 8889

# BOILERPLATE from python docs

loop = asyncio.get_event_loop()
coro = asyncio.start_server(request_handler, HOSTNAME, PORT, loop=loop)
server = loop.run_until_complete(coro)

        # Serve requests until CTRL+c is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
