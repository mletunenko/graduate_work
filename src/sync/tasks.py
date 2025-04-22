import json

from aio_pika import Message
from aio_pika.abc import AbstractChannel

from core.consts import CREATE_USER_QUEUE, DELETE_USER_QUEUE
from models import ProfileModel
from schemas.profile import ProfileIn


async def create_user_task(
    data: ProfileIn,
    rabbit_channel: AbstractChannel,
):
    body = {"email": data.email, "password": data.password}
    json_body = json.dumps(body)
    await rabbit_channel.default_exchange.publish(
        Message(body=json_body.encode()),
        routing_key=CREATE_USER_QUEUE,
    )


async def delete_user_task(
    data: ProfileModel,
    rabbit_channel: AbstractChannel,
):
    body = {
        "email": data.email,
    }
    json_body = json.dumps(body)
    await rabbit_channel.default_exchange.publish(
        Message(body=json_body.encode()),
        routing_key=DELETE_USER_QUEUE,
    )
