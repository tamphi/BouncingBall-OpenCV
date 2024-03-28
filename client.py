import multiprocessing as mp
import argparse
import asyncio
import time

from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import BYE, create_signaling
from aiortc.contrib.media import MediaBlackhole
from src.display import display_and_queue_images
from src.consume import consume_signaling

time_start = None

def current_stamp():
    global time_start
    if time_start is None:
        time_start = time.time()
        return 0
    else:
        return int((time.time() - time_start) * 1000000)
    
async def run_answer(pc, signaling, queue):
    await signaling.connect()

    @pc.on('track')
    async def on_track(track):
        #to do: display frames
        await display_and_queue_images(track, queue)
        

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            # print(message)
            if isinstance(message, str) and message.startswith("image"):
                # reply
                msg = f"value $DUMMY$ time {current_stamp()}"
                channel.send(msg)

    await consume_signaling(pc, signaling)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="client")
    parser.add_argument( "--signaling", default = "tcp-socket")
    parser.add_argument("--signaling-host", default="127.0.0.1", help="Signaling host (tcp-socket only)")
    parser.add_argument("--signaling-port", default="8080", help="Signaling port (tcp-socket only)")

    args = parser.parse_args()

    # create signaling and peer connection
    signaling = create_signaling(args)
    pc = RTCPeerConnection()

    # create media sink
    recorder = MediaBlackhole()

    #create queue to store video frames
    # mp.set_start_method('spawn')
    duration = 10 # second
    n_frame = 30 # number of frames of BallVideoStreamTrack class
    queue = None
    # queue = mp.Queue(duration*n_frame)
    #send answer
    coro = run_answer(pc, signaling, queue)

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())

