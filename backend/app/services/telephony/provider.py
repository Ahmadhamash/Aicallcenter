from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IncomingCallEvent:
    provider_call_id: str
    branch_id: int
    from_number: str
    audio_codec: str = 'pcm16'


class TelephonyProvider(ABC):
    @abstractmethod
    async def accept_call(self, event: IncomingCallEvent) -> None: ...

    @abstractmethod
    async def stream_audio_to_bridge(self, provider_call_id: str, audio_chunk: bytes) -> None: ...

    @abstractmethod
    async def play_audio_to_caller(self, provider_call_id: str, audio_chunk: bytes) -> None: ...

    @abstractmethod
    async def transfer_call(self, provider_call_id: str, target: str) -> None: ...


class MockTelephonyProvider(TelephonyProvider):
    async def accept_call(self, event: IncomingCallEvent) -> None:
        return None

    async def stream_audio_to_bridge(self, provider_call_id: str, audio_chunk: bytes) -> None:
        return None

    async def play_audio_to_caller(self, provider_call_id: str, audio_chunk: bytes) -> None:
        return None

    async def transfer_call(self, provider_call_id: str, target: str) -> None:
        return None
