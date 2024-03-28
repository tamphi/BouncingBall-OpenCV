from aiortc import RTCIceCandidate, RTCSessionDescription
from aiortc.contrib.signaling import BYE

async def consume_signaling(pc, signaling):
    """
    Ping offer and pong answer signals
    """
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
            #pong answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break