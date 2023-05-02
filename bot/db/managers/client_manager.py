from typing import Optional

from sqlalchemy import select, update

from bot.db.models import Client
from bot.utils.config import async_session
from bot.utils.misc import error_handler


class ClientManager(object):
    @classmethod
    @error_handler
    async def update(cls, user_id, name=None, username=None, phone_number=None) -> Optional[Client]:
        async with async_session() as session:
            update_instance = update(Client).where(Client.user_id == user_id).values(
                user_id=user_id, name=name,
                username=username, phone_number=phone_number)
            await session.execute(update_instance)
            await session.commit()
            return update_instance.is_update

    @classmethod
    @error_handler
    async def create(cls, user_id, name, username=None, phone_number=None) -> Optional[Client]:
        async with async_session() as session:
            client_obj = Client(user_id=user_id, name=name,
                                username=username, phone_number=phone_number)
            session.add(client_obj)
            await session.commit()
            return client_obj

    @classmethod
    @error_handler
    async def update_or_create(cls, user_id, name, username=None, phone_number=None) -> Optional[Client]:
        async with async_session() as session:
            instance = select(Client).where(Client.user_id == user_id)
            if client := await session.scalar(instance):
                await cls.update(user_id, name, username, phone_number)
                return client
            return await cls.create(user_id, name, username, phone_number)

    @classmethod
    @error_handler
    async def get_all_clients(cls):
        async with async_session() as session:
            clients = select(Client)
            return await session.scalars(clients)

    @classmethod
    @error_handler
    async def get_client_by_id(cls, user_id):
        async with async_session() as session:
            client = select(Client).where(Client.user_id == user_id)
            return await session.scalar(client)
