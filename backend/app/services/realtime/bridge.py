import asyncio
import json
import time
from collections import defaultdict

import websockets

from app.core.config import settings


class RealtimeBridge:
    def __init__(self):
        self.session_state: dict[str, dict] = defaultdict(dict)

    async def connect(self, session_id: str) -> websockets.WebSocketClientProtocol:
        ws = await websockets.connect(
            f"wss://api.openai.com/v1/realtime?model={settings.openai_realtime_model}",
            extra_headers={
                'Authorization': f'Bearer {settings.openai_api_key}',
                'OpenAI-Beta': 'realtime=v1',
            },
        )
        self.session_state[session_id] = {'connected_at': time.time(), 'latencies_ms': []}
        return ws

    async def stream_audio_bidirectional(self, session_id: str, audio_source):
        ws = await self.connect(session_id)
        try:
            async for chunk in audio_source:
                t0 = time.time()
                await ws.send(
                    json.dumps(
                        {'type': 'input_audio_buffer.append', 'audio': chunk.hex()}
                    )
                )
                await ws.send(json.dumps({'type': 'response.create'}))
                _ = await ws.recv()
                latency = (time.time() - t0) * 1000
                self.session_state[session_id]['latencies_ms'].append(latency)
        except Exception:
            await asyncio.sleep(0.2)
            # simple reconnect strategy
            await self.connect(session_id)
        finally:
            await ws.close()

    async def handle_function_call(self, tool_name: str, arguments: dict) -> dict:
        handlers = {
            'get_restaurant_menu': lambda args: {'ok': True, 'items': []},
            'check_item_availability': lambda args: {'ok': True, 'available': True},
            'calculate_total_price': lambda args: {'ok': True, 'total': 0},
            'create_order': lambda args: {'ok': True, 'order_id': 0},
            'print_receipt': lambda args: {'ok': True, 'print_status': 'queued'},
            'transfer_to_human_agent': lambda args: {'ok': True, 'handoff': 'initiated'},
            'log_complaint': lambda args: {'ok': True},
            'cancel_or_refund_request': lambda args: {'ok': True},
        }
        if tool_name not in handlers:
            return {'ok': False, 'error': 'unsupported tool'}
        return handlers[tool_name](arguments)
