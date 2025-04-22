import asyncio
import json
import logging

import aio_pika
import aiohttp

from core.config import settings

logger = logging.getLogger("profile-worker")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Логи в файл
        logging.StreamHandler(),  # Логи в консоль (для Docker)
    ],
)
logger = logging.getLogger(__name__)


async def process_update_email(message: aio_pika.IncomingMessage):
    try:
        message_data = json.loads(message.body.decode())
        update_email_url = f"http://{settings.profile_service.host}:{settings.profile_service.port}{settings.profile_service.update_email_path}"
        logger.info(f"message_data: {message_data}")
        async with aiohttp.ClientSession() as session:
            await session.post(update_email_url, json=message_data)
        await message.ack()

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.nack(requeue=False)


async def consume():
    logger.info(f"settings.rabbit.host: {settings.rabbit.host}")
    connection = await aio_pika.connect_robust(
        host=settings.rabbit.host,
        login=settings.rabbit.login,
        password=settings.rabbit.password,
    )

    async with connection:
        channel = await connection.channel()
        update_email_queue = await channel.declare_queue("update_email", durable=True)
        await update_email_queue.consume(process_update_email, no_ack=False)

        await asyncio.Future()


if __name__ == "__main__":
    logger.info("Запуск воркера сервиса Профили...")
    asyncio.run(consume())
