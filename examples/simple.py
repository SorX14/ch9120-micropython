import asyncio
from machine import UART, Pin
from ch9120server import CH9120Server
from microdot import Microdot, send_file
import os

# Important to set `rxbuf` otherwise `sreader.readline` will truncate responses
uart = UART(1, baudrate=921600, tx=Pin(20), rx=Pin(21), timeout_char=1, rxbuf=2048)
app = Microdot()
server = CH9120Server(app, uart)
  
@app.route('/')
async def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>CH9120 example</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>Hello world!</h1>
    <img src="/img" />
  </body>
</html>''', 200, {'Content-Type': 'text/html'}
    
@app.route('/img')
async def static(request):
    # There is no 'close' event, so the browser will wait forever instead of finishing
    # We'll add the exact length of the file being provided
    @request.after_request
    def reset_session(request, response):
        response.headers['Content-Length'] = os.stat('img.png')[6]
        return response
    return send_file('img.png')
    
asyncio.run(server.start())
