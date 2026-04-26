"""Simulate incoming telephony calls for local development."""

import asyncio

from app.services.realtime.bridge import RealtimeBridge
from app.services.telephony.gateway import TelephonyGateway
from app.services.telephony.provider import IncomingCallEvent, MockTelephonyProvider


async def main() -> None:
    gateway = TelephonyGateway(provider=MockTelephonyProvider(), bridge=RealtimeBridge())
    event = IncomingCallEvent(provider_call_id='mock-call-001', branch_id=1, from_number='+962790000002')
    await gateway.handle_incoming_call(event)
    print('Mock call processed.')


if __name__ == '__main__':
    asyncio.run(main())
