import argparse
import asyncio
import time
import logging

from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from src.media import BallVideoStreamTrack
from src.consume import consume_signaling

## source aiortc 

time_start = None
def current_stamp():
    global time_start

    if time_start is None:
        time_start = time.time()
        return 0
    else:
        return int((time.time() - time_start) * 1000000)
def calculate_error(message, ball_video_track):
    message = message.strip().split(" ")
    predictedX = float(message[1])
    predictedY = float(message[2])
    trueX = float(ball_video_track.x)
    trueY = float(ball_video_track.y)
    errorX = round(float(abs(predictedX-trueX)),3)
    errorY = round(float(abs(predictedY-trueY)),3)

    prediction_msg = f"(x,y) prediction ({predictedX}, {predictedY}),"
    true_msg = f"true ({trueX}, {trueY})"
    error_msg = f"error ({errorX}, {errorY})"

    print(prediction_msg, true_msg, error_msg)

async def run_offer(pc, signaling, recorder):
    """
    Transmit moving ball animation to client & calculate prediction error from client's answer

    Keyword arguments:
    pc: peer connection
    signaling: signaling method (tcp, unix, copy & paste)
    recorder: media sink object
    """

    #create data channel
    channel = pc.createDataChannel("chat")
    #intialize ball object
    ball_video_track = BallVideoStreamTrack()

    @pc.on('track')
    def on_track(track):
        # add track to be recorded or to sink
        recorder.addTrack(track)
        
        @track.on('ended')
        async def on_ended():
            # stop recording
            recorder.stop()
            
    @channel.on("open")
    def on_open():
        channel_msg = f"frame {current_stamp()}"
        channel.send(channel_msg)

    @channel.on("message")
    def on_message(message):
        # print(f'[SERVER] Received message: {message}')
        if isinstance(message, str) and message.startswith("prediction"):
            calculate_error(message,ball_video_track)
            channel_msg = f"frame {current_stamp()}"
            # print(f"[SERVER] offer: {channel_msg}", 1)
            channel.send(channel_msg)
        
    await signaling.connect()
    #add media
    pc.addTrack(ball_video_track)
    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)
    await consume_signaling(pc, signaling)
    print('[SERVER] send tracks to the client')

if __name__ == "__main__":

    #host and port for tcp-socket
    parser = argparse.ArgumentParser(description="server")
    parser.add_argument( "--signaling", default = "tcp-socket", help ="Signaling method (tcp-socket or unix-socket)", type = str)
    parser.add_argument("--signaling-host", default="127.0.0.1", help="Signaling host (tcp-socket only)", type = str)
    parser.add_argument("--signaling-port", default="8080", help="Signaling port (tcp-socket only)", type = str)

    args = parser.parse_args()

    # create signaling and peer connection
    signaling = create_signaling(args)
    pc = RTCPeerConnection()

    # create media sink
    recorder = MediaBlackhole()

    #send offer
    coro = run_offer(pc, signaling, recorder)

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())

