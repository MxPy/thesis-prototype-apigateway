import aio_pika
import logging
from q.settings import settings
from typing import AsyncGenerator
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from websocket.connectionManager import manager
from q.messages import *
import json
from typing import Dict, List

logger = logging.getLogger()

activeUsersTemplate = Dict[str, List[str]]
activeUsers: activeUsersTemplate = {}

activeQueuesTemplate = List[str]
activeQueues: activeQueuesTemplate = ["Test", "HealthData", "Logs", "Moderation"]


async def get_amqp_connection() -> aio_pika.abc.AbstractConnection:
    """Connect to AMQP server."""
    return await aio_pika.connect_robust(str(settings.AMQP_URL))

async def add_user_to_active_users(user_id: str, session_id: str):
    """
    Add user session to active users dictionary.
    
    Args:
        user_id: User identifier
        session_id: Session identifier
    """
    logger.info(f"Adding user {user_id} with session {session_id} to active users")
    
    if user_id not in activeUsers:
        activeUsers[user_id] = []
    
    if session_id not in activeUsers[user_id]:
        activeUsers[user_id].append(session_id)
    
    logger.debug(f"Active users after addition: {activeUsers}")

async def remove_user_from_active_users(user_id: str, session_id: str):
    """
    Remove user session from active users dictionary.
    
    Args:
        user_id: User identifier
        session_id: Session identifier
    """
    logger.info(f"Removing user {user_id} with session {session_id} from active users")
    
    if user_id in activeUsers:
        if session_id in activeUsers[user_id]:
            activeUsers[user_id].remove(session_id)
            
            # If user has no active sessions, remove user entry
            if not activeUsers[user_id]:
                del activeUsers[user_id]
    
    logger.debug(f"Active users after removal: {activeUsers}")

async def declare_queue(
    channel: aio_pika.abc.AbstractChannel,
    queue: str,
    **kwargs,
) -> aio_pika.abc.AbstractQueue:
    """Create AMQP queue."""
    logger.debug(f"Queue {queue} declarated!!!")
    return await channel.declare_queue(name=queue, auto_delete=True, **kwargs)
        
async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    """Do something with the message.
w
    :param message: A message from the queue.
    """
    try:
        async with message.process(requeue=True):
            jmsg = json.loads(message.body.decode())
            logger.info(f"MESSAGE RECEIVED: {jmsg['type']}")
            logger.info(f"{jmsg}")
            if int(jmsg['type']) == 0:
                jmsg = DirectMessage(**jmsg)
                if activeUsers.get(jmsg.target):
                    for session in activeUsers.get(jmsg.target):
                        await manager.broadcast(session, jmsg.data.model_dump())
                else:
                    pass
    except Exception as e:
        logger.error(e)
        
        
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start internal message consumer on app startup."""
    connection = await aio_pika.connect_robust(str(settings.AMQP_URL))
    logger.debug("Rabbit connected")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=settings.PREFECTH_COUNT)
        queues = [await declare_queue(channel=channel, queue=queue) for queue in activeQueues]
        for queue in queues:
            await queue.consume(process_message) 
        yield

async def get_channel(
    connection: aio_pika.abc.AbstractConnection = Depends(get_amqp_connection)
) -> AsyncGenerator[aio_pika.abc.AbstractChannel, None]:
    """Connect to and yield a AMQP channel.

    :yield: RabbitMQ channel.
    """
    async with connection:
        channel = await connection.channel()
        queues = [await declare_queue(channel=channel, queue=queue) for queue in activeQueues]
        yield channel

async def publish_message(
    type: int,
    target: str,
    data: str,
    channel: aio_pika.abc.AbstractChannel,
):
    """Publish a message to the event queue.

    :param message: A message to publish.
    :param channel: The AMQP channel to publish the message to.
    """
    msg = aio_pika.Message(
        body=DirectMessage(type=type, target=target, data=MessageData(type=0, data=data)).model_dump_json().encode(),
    )
    await channel.default_exchange.publish(
        msg,
        routing_key="Test",
    )

    return msg
