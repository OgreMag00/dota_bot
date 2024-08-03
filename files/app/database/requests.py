from .models import async_session
from .models import User
from sqlalchemy import select, update

async def set_user(tg_id: int, dota_id: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, dota_id=dota_id))
            await session.commit()
            

async def get_dota_id(tg_id: int):
    async with async_session() as session:
        res = await session.execute(select(User).where(User.tg_id == tg_id))
        user = res.scalar_one()
       
        
        return user.dota_id

async def check_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return True
        else:
            return False
        
async def update_dota_id(tg_id: int, new_dota_id: str):
    async with async_session() as session:
        res = await session.scalar(select(User).where(User.tg_id == tg_id))
        res.dota_id = new_dota_id
        await session.commit()