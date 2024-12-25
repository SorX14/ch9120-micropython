# CH9120 Micropython library

## About

After purchasing a [Waveshare RP2350-ETH](https://www.waveshare.com/rp2350-eth.htm), I wanted to be able to use
a webserver, specifically [Microdot](https://microdot.readthedocs.io/en/latest/).

Tried writing my own ASGI webserver, attempting to fake sockets and other time-wasting ventures, I settled on
providing a `StreamReader` and `StreamWriter` with UART which is _mostly_ compatible with TCP sockets.

## Usage

Use the 'Network configuration tool' as provided on the Waveshare wiki page to configure your device to be in
TCP server mode.

Follow the Microdot installation tasks, specifically:

- Create 'microdot' folder on your RP2350
- Add `__init__.py` and `microdot.py`

Grab the `ch9120server.py` and add to the root of your device.

Try one of the examples!

## Limitations

As the CH9120 is a transparent TCP to UART converter, there are several limitations that make it much less powerful
compared to a full stack, specifically:

- Only one connection can be served at once
- The socket close event doesn't exist - e.g the Microdot video feed streaming example has odd behavour, or images need a content length header attached
- The peer IP cannot be determined
- You need to set up the CH9120 separately
