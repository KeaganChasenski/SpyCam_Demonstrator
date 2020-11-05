## Installation

Then make sure you've got the following packages
installed:

    $ sudo apt-get install ffmpeg git python3-picamera python3-ws4py python3-pantilthat

Next, clone this repository:

    $ git clone https://github.com/waveform80/pistreaming.git


## Usage

Run the Python server script which should print out a load of stuff
to the console as it starts up:

    $ cd pistreaming
    $ python3 server.py
    Initializing HAT
    Initializing websockets server on port 8084
    Initializing HTTP server on port 8082
    Initializing camera
    Initializing broadcast thread
    Spawning background conversion process
    Starting websockets thread
    Starting HTTP server thread
    Starting broadcast thread

Now fire up your favourite web-browser and visit the address
`http://pi-address:8082/` - it should fairly quickly start displaying the feed
from the camera. You should be able to visit the URL from multiple browsers
simultaneously (although obviously you'll saturate the Pi's bandwidth sooner or
later).

If you find the video stutters or the latency is particularly bad (more than a
second), please check you have a decent network connection between the Pi and
the clients. I've found ethernet works perfectly (even with things like
powerline boxes in between) but a poor wifi connection doesn't provide enough
bandwidth, and dropped packets are not handled terribly well.

To shut down the server press Ctrl+C - you may find it'll take a while
to shut down unless you close the client web browsers (Chrome in particular
tends to keep connections open which will prevent the server from shutting down
until the socket closes).



### HTTP server

This is implemented in the `StreamingHttpServer` and `StreamingHttpHandler`
classes, and is quite simple:

* In response to an HTTP GET request for "/" it will redirect the client to
  "/index.html".
* In response to an HTTP GET request for "/index.html" it will serve up the
  contents of index.html, replacing @ADDRESS@ with the Pi's IP address and
  the websocket port.
* In response to an HTTP GET request for "/jsmpg.js" it will serve up the
  contents of jsmpg.js verbatim.
* In response to an HTTP GET request for "/do_orient?pan=0&tilt=0" it will
  orient the pan-tilt HAT to the specified values; the sliders present in
  "index.html" are hooked to some JavaScript which will make such requests
* In response to an HTTP GET request for anything else, it will return 404.
* In response to an HTTP HEAD request for any of the above, it will simply
  do the same as for GET but will omit the content.
* In response to any other HTTP method it will return an error.


### Websockets server

This is implemented in the `StreamingWebSocket` class and is ridiculously
simple. In response to a new connection it will immediately send a header
consisting of the four characters "jsmp" and the width and height of the video
stream encoded as 16-bit unsigned integers in big-endian format. This header is
expected by the jsmpg implementation. Other than that, the websocket server
doesn't do much. The actual broadcasting of video data is handled by the
broadcast thread object below.


### Broadcast output

The `BroadcastOutput` class is an implementation of a [picamera custom
output](http://picamera.readthedocs.org/en/latest/recipes2.html#custom-outputs).
On initialization it starts a background FFmpeg process (`avconv`) which is
configured to expect raw video data in YUV420 format, and will encode it as
MPEG1. As unencoded video data is fed to the output via the `write` method, the
class feeds the data to the background FFmpeg process.


### Broadcast thread

The `BroadcastThread` class implements a background thread which continually
reads encoded MPEG1 data from the background FFmpeg process started by the
`BroadcastOutput` class and broadcasts it to all connected websockets. In the
event that no websockets are currently connected the `broadcast` method simply
discards the data. In the event that no more data is available from the FFmpeg
process, the thread checks that the FFmpeg process hasn't finished (with
`poll`) and terminates if it has.


### Main

Finally, the `main` method may look long and complicated but it's mostly
boiler-plate code which constructs all the necessary objects, wraps several of
them in background threads (the HTTP server gets one, the main websockets
server gets another, etc.), configures the camera and starts it recording to
the `BroadcastOutput` object. After that it simply sits around calling
`wait_recording` until someone presses Ctrl+C, at which point it shuts
everything down in an orderly fashion and exits.
