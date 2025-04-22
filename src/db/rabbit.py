from typing import Annotated

import aio_pika
from aio_pika.abc import AbstractChannel
from fastapi import Depends

from core.config import settings
from core.consts import CREATE_USER_QUEUE, DELETE_USER_QUEUE


class RabbitMQConnection:
    def __init__(self) -> None:
        self.connection = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(
                host=settings.rabbit.host,
                login=settings.rabbit.login,
                password=settings.rabbit.password,
            )
        return self.connection

    async def get_channel(self):
        connection = await self.connect()
        return await connection.channel()

    async def close(self):
        if self.connection:
            self.connection.close()

    async def declare_queues(self):
        channel = await self.get_channel()
        await channel.declare_queue(CREATE_USER_QUEUE, durable=True)
        await channel.declare_queue(DELETE_USER_QUEUE, durable=True)
        # delete from ugc


rabbitmq = RabbitMQConnection()


async def get_rabbitmq_channel():
    async with await rabbitmq.get_channel() as channel:
        yield channel


RabbitDep = Annotated[AbstractChannel, Depends(get_rabbitmq_channel)]
