from sqlalchemy import select

from db import AsyncSessionLocal, RequestsInfo


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(
        self,
        info: dict,
    ):
        obj = self.model(**info)
        async with AsyncSessionLocal() as session:
            session.add(obj)
            await session.commit()

    async def get(
        self,
        obj_id: int,
    ):
        async with AsyncSessionLocal() as session:
            db_obj = await session.execute(
                select(self.model).where(self.model.user_id == obj_id)
            )
        return db_obj.scalars().first()


requests_info_crud = CRUDBase(RequestsInfo)
