"""Create and configure a local SQLite database"""
import sqlalchemy
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


engine = create_engine("sqlite://", echo=True)

class DB:
    def __init__(self):
        self.engine = engine
        
class Base(DeclarativeBase):
    pass

# Entity (player, mob, item, etc) and related tables

class GameEntity(Base):
    __tablename__ = "game_entity"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(64))
    
    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, name={self.name!r})"

class Item(Base):
    """Lookup table for in game items"""
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, name={self.name!r})"

class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    entity_id = mapped_column(ForeignKey("game_entity.id"))
    
    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, entity_id={self.entity_id!r})"

class InventoryItem(Base):
    """Junction table between inventories and items"""
    __tablename__ = "inventory_item"
    inventory_id = mapped_column(ForeignKey("inventory.id"), primary_key=True)
    item_id = mapped_column(ForeignKey("item.id"), primary_key=True)
    count: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"RoomWall(inventory_id={self.inventory_id!r}, item_id={self.item_id!r}, count={self.count!r})"

# Room/Door tables

class RoomWall(Base):
    """Static table to help with wall naming/pairing"""
    __tablename__ = "room_wall"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    side: Mapped[str] = mapped_column(String(5)) # north, east, south, west
    pair: Mapped[int] = mapped_column()        
        
    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, side={self.side!r}, pair={self.pair!r})"

class DungeonTile(Base):
    """Dungeon Tile class"""
    __tablename__ = "dungeon_tile"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Dungeon(id={self.id!r}, room_id={self.room_id!r})"

class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, x={self.x!r}, y={self.y!r})"
    
class Door(Base):
    __tablename__ = "door"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Door(id={self.id!r}, room_id={self.room_id!r})"

class RoomDoor(Base):
    __tablename__ = "room_door"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_wall_id: Mapped[int] = mapped_column() # TODO: make this second PK
    door_id: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"RoomDoor(id={self.id!r}, room_wall_id={self.room_wall_id!r}, door_id={self.door_id!r})"



def main() -> None:
    Base.metadata.create_all(engine)



if __name__ == "__main__":
    main()