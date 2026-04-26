import pytest

from app.services.realtime.bridge import RealtimeBridge


@pytest.mark.asyncio
async def test_handle_function_call_mock():
    bridge = RealtimeBridge()
    out = await bridge.handle_function_call('transfer_to_human_agent', {'reason': 'angry'})
    assert out['ok'] is True
    assert out['handoff'] == 'initiated'


@pytest.mark.asyncio
async def test_handle_function_call_unsupported():
    bridge = RealtimeBridge()
    out = await bridge.handle_function_call('unknown_tool', {})
    assert out['ok'] is False
