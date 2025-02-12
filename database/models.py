from sqlalchemy import BigInteger, String, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

#Создание базы данных (sqlite)

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Registered(Base):
    __tablename__ = 'registered'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    tg_id = Column(BigInteger, nullable=False)
    surname: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(25))
    phone_number: Mapped[str] = mapped_column(String(25))
    birth_date: Mapped[str] = mapped_column(String(25))
    InQueue: Mapped[bool] = mapped_column()
    
#если нет таблицы, создаёт её

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)