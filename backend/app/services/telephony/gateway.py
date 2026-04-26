from app.services.realtime.bridge import RealtimeBridge
from app.services.telephony.provider import IncomingCallEvent, TelephonyProvider


class TelephonyGateway:
    def __init__(self, provider: TelephonyProvider, bridge: RealtimeBridge):
        self.provider = provider
        self.bridge = bridge

    async def handle_incoming_call(self, event: IncomingCallEvent):
        await self.provider.accept_call(event)
        # TODO: connect real RTP/SIP media stream here.
        async def fake_audio_source():
            for _ in range(3):
                yield b'\\x00\\x01'
        await self.bridge.stream_audio_bidirectional(event.provider_call_id, fake_audio_source())
