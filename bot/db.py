import os
from typing import Optional
from sqlalchemy import (
    MetaData, Table, Column, String, BigInteger, Integer, Text, DateTime, func
)
from sqlalchemy import create_engine
from databases import Database

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./dev.db')

database = Database(DATABASE_URL)
metadata = MetaData()

# Tickets table schema (minimal viable)
tickets = Table(
    'tickets',
    metadata,
    Column('ticket_id', String(64), primary_key=True),
    Column('user_id', BigInteger, nullable=False),
    Column('guild_id', BigInteger, nullable=False),
    Column('channel_id', BigInteger, nullable=False),
    Column('category', String(120)),
    Column('status', String(50), nullable=False, server_default='open'),
    Column('claimed_by', BigInteger, nullable=True),
    Column('notes', Text, nullable=True),
    Column('created_at', DateTime, server_default=func.now()),
    Column('closed_at', DateTime, nullable=True),
)


async def connect():
    await database.connect()


async def disconnect():
    await database.disconnect()


def create_tables():
    """Create tables synchronously (for initial migration / local dev)."""
    engine = create_engine(DATABASE_URL, future=True)
    metadata.create_all(engine)


async def create_ticket(ticket_id: str, user_id: int, channel_id: int, guild_id: int, category: Optional[str] = None):
    query = tickets.insert().values(
        ticket_id=ticket_id,
        user_id=user_id,
        channel_id=channel_id,
        guild_id=guild_id,
        category=category,
    )
    await database.execute(query)


async def get_ticket(ticket_id: str):
    query = tickets.select().where(tickets.c.ticket_id == ticket_id)
    return await database.fetch_one(query)


async def get_channel_ticket(channel_id: int):
    query = tickets.select().where(tickets.c.channel_id == channel_id)
    row = await database.fetch_one(query)
    if not row:
        return None
    return row['ticket_id']


async def get_user_tickets(user_id: int, guild_id: int):
    query = tickets.select().where(
        (tickets.c.user_id == user_id) &
        (tickets.c.guild_id == guild_id) &
        (tickets.c.status != 'closed')
    )
    return await database.fetch_all(query)


async def update_ticket(ticket_id: str, **fields):
    if not fields:
        return
    query = tickets.update().where(tickets.c.ticket_id == ticket_id).values(**fields)
    await database.execute(query)


async def close_ticket(ticket_id: str, closed_by: Optional[int] = None):
    values = {'status': 'closed', 'closed_at': func.now()}
    if closed_by:
        values['claimed_by'] = closed_by
    query = tickets.update().where(tickets.c.ticket_id == ticket_id).values(**values)
    await database.execute(query)
