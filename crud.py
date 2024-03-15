"""Модуль операций CRUD."""

from sqlalchemy import select

from db import AsyncSessionLocal, RequestsInfo


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(
        self,
        info: dict,
    ):
        """запись в базу объекта класса."""
        obj = self.model(**info)
        async with AsyncSessionLocal() as session:
            session.add(obj)
            await session.commit()

    async def get(
        self,
        obj_id: int,
    ):
        """получение пяти последних объектов класса."""
        async with AsyncSessionLocal() as session:
            db_obj = await session.execute(
                select(self.model)
                .where(self.model.user_id == obj_id)
                .order_by(self.model.create_date.desc())
                .limit(5)
            )
        return db_obj.scalars().all()


requests_info_crud = CRUDBase(RequestsInfo)
