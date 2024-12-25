import asyncio
from machine import Pin
import time

class CH9120Server:
    def __init__(self, app, uart, resetpin=19, debug=True):
        self.app = app
        self.debug = debug
        
        RSTI = Pin(resetpin, Pin.OUT)
       
        if debug:
            print('Resetting interface...')
        RSTI.value(0)
        time.sleep(0.1)
        RSTI.value(1)
        time.sleep(0.5)
        
        if debug:
            print('Done!')
        
        class WriterWrapper(asyncio.StreamWriter):   
            async def aclose(self):
                if debug:
                    print("aclose")
                return
            
            def get_extra_info(self, item):
                return '0.0.0.0'
        
        self.sreader = asyncio.StreamReader(uart)
        self.swriter = WriterWrapper(uart, {})
    
    async def serve(reader, writer):
        await self.app.handle_request(reader, writer)

    async def listen_for_data(self, loop):
        if self.debug:
            print('Listening for data')
        while True:
            await self.app.handle_request(self.sreader, self.swriter)
            
    async def start(self):
        loop = asyncio.get_event_loop()
        await self.listen_for_data(loop)