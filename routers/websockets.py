from fastapi import WebSocket, WebSocketDisconnect, HTTPException, APIRouter, Depends
from auth import decode_access_token, decode_access_token_admin
from websocket.connectionManager import manager
from q.queueManager import add_user_to_active_users, remove_user_from_active_users, activeUsers, publish_message, get_channel
import logging
import aio_pika
router = APIRouter(prefix='/socket', tags=['socket'])

logger = logging.getLogger()


@router.websocket("/connect/{user_id}")
async def user_connect(user_id: str, websocket: WebSocket):
    protocols = websocket.headers.get('sec-websocket-protocol', '').split(', ')
    logger.info(f"try to connect user_id: {user_id}")
    session_id = None
    for protocol in protocols:
        if protocol.startswith('session-id.'):
            session_id = protocol.replace('session-id.', '')
            break
    logger.info(f"try to connect session_id: {session_id}")
    if not session_id:
        await websocket.close(code=4001)
        return

    auth = await decode_access_token(session_id)
    if not auth.get("valid"):
        await websocket.close(code=403)
        return
    logger.info(f"valid session token")
    
    await manager.connect(session_id, websocket)
    await add_user_to_active_users(user_id, session_id)
    try:
        while True:
            data = await websocket.receive_json()
            #await manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(session_id, websocket)
        await remove_user_from_active_users(user_id, session_id)

@router.websocket("/connect-a/{user_id}")
async def user_connect(user_id: str, websocket: WebSocket):
    protocols = websocket.headers.get('sec-websocket-protocol', '').split(', ')
    logger.info(f"try to connect user_id: {user_id}")
    session_id = None
    for protocol in protocols:
        if protocol.startswith('session-id.'):
            session_id = protocol.replace('session-id.', '')
            break
    logger.info(f"try to connect session_id: {session_id}")
    if not session_id:
        await websocket.close(code=4001)
        return

    auth = await decode_access_token_admin(session_id)
    if not auth.get("valid"):
        await websocket.close(code=403)
        return
    logger.info(f"valid session token")
    
    await manager.connect(session_id, websocket)
    await add_user_to_active_users(user_id, session_id)
    try:
        while True:
            data = await websocket.receive_json()
            #await manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(session_id, websocket)
        await remove_user_from_active_users(user_id, session_id)
