# Architecture

## Core event-driven components

- `CallSession`: persisted lifecycle for each voice call.
- `ConversationState`: in-memory session state (confidence, misunderstanding count, escalation flag).
- `OrderStateMachine`: deterministic flow from GREETING to END_CALL.
- `MenuToolService`: tool functions for menu retrieval, availability checks, price totals.
- `EscalationService`: business rules for immediate human transfer.
- `ReceiptPrinterService`: pluggable printing adapter (mock implemented).
- `HumanHandoffService`: persistence of transfer requests and reasons.
- `RealtimeBridge`: OpenAI Realtime WebSocket bridge and tool call router.
- `TelephonyGateway`: adapter that binds provider streams to realtime bridge.
- `RestaurantConfigService`: tenant-aware Arabic prompt and dialect switching.

## Telephony abstraction

`TelephonyProvider` is an interface that can be implemented for SIP providers, Asterisk/FreePBX, Amazon Connect, or custom PBX. No provider-specific logic is hardcoded in domain services.

## Tenant isolation

All tenant-owned records include `restaurant_id` so API handlers and repository methods can enforce data isolation boundaries per restaurant.

## OpenAI Realtime notes

- Backend uses WebSocket transport for server-to-server bridge.
- Designed for barge-in/interruption by maintaining active session state and streaming chunk loop.
- Function tools map to backend capabilities.
- Reconnect path included to avoid call drop on transient network failures.
