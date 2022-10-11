from asyncio import BaseProtocol, BaseTransport
from typing import Tuple

import aioamqp

class SubscriberMQ:

    @staticmethod
    async def mq_handler(channel, message_body, envelope, properties):
        print(f'Notification collected: {message_body}')

    @staticmethod
    async def get_mq_connection() -> Tuple[BaseTransport, BaseProtocol]:
        try:
            base_transport, base_protocol =  await aioamqp.connect(
                login='admin', password='test'
            )
            return base_transport, base_protocol
        except aioamqp.AmqpClosedConnection:
            print('Connection has been closed')
            return

    async def consume_queue(
            self,
            queue_name: str,
            app: FastAPI,
            durable: bool = True,
            no_ack: bool = True
    ):
        _, base_protocol = await self.get_mq_connection()
        app.mq_channel = await base_protocol.channel()
        await app.mq_channel.queue_declare(queue_name, durable=durable)
        await app.mq_channel.basic_consume(
            self.mq_handler, queue_name=queue_name, no_ack=no_ack
        )

mq_subscriber = SubscriberMQ()