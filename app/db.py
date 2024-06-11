"""Create and configure a local SQLite database"""
import sqlalchemy
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Session


engine = create_engine("sqlite://", echo=True)

class DB:
    def __init__(self):
        self.engine = engine
        
class Base(DeclarativeBase):
    pass

# Settings
class Settings(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    yaml_file: Mapped[str] = mapped_column(String(64))
    
    def __repr__(self) -> str:
        return f"Settings(id={self.id!r}, yaml_file={self.yaml_file!r})"
    
# GameEntity (player, mob, item, etc)
class GameEntity(Base):
    __tablename__ = "game_entity"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(64))
    
    def __repr__(self) -> str:
        return f"GameEntity(id={self.id!r}, name={self.name!r})"

def create_game_entity(id, name):
        with Session(engine) as session:
            game_entity = GameEntity(id = id, name = name)
        session.add(game_entity)
        session.commit()

def read_game_entity():
    pass

def update_game_entity():
    pass

def delete_game_entity():
    pass

# FilePath
class FilePath(Base):
    __tablename__ = "file_path"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    file_name: Mapped[str] = mapped_column(String(256))
    extension: Mapped[str] = mapped_column(String(32))

    def __repr__(self) -> str:
        return f"FilePath(id={self.id!r}, file_name={self.file_name!r}, extension={self.extension!r})"

# Sprite
class Sprite(Base):
    __tablename__ = "sprite"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    file_path_id: Mapped[int] = mapped_column(ForeignKey("file_path.id"))
    
    def __repr__(self) -> str:
        return f"Sprite(id={self.id!r}, file_path_id={self.file_path_id!r})"

# SpriteSet
class SpriteSet(Base):
    __tablename__ = "sprite_set"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    file_path_id: Mapped[int] = mapped_column(ForeignKey("file_path.id"))
    subsheets_start: Mapped[int] = mapped_column()
    subsheets_end: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"SpriteSet(id={self.id!r}, file_path_id={self.file_path_id!r})"
    
# Character
class Character(Base):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    game_entity_id: Mapped[int] = mapped_column(ForeignKey("game_entity.id"))
    sprite_set_id: Mapped[int] = mapped_column(ForeignKey("sprite_set.id"))
    name: Mapped[str] = mapped_column(String(64))
    max_hp: Mapped[int] = mapped_column()
    atk: Mapped[int] = mapped_column()
    dex: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}) ..."
    
# Player
class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    player_color: Mapped[str] = mapped_column(String(32))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, character_id={self.character_id!r})"

# Monster
class Monster(Base):
    __tablename__ = "monster"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    monster_color: Mapped[str] = mapped_column(String(32))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, character_id={self.character_id!r})"

# Item
class Item(Base):
    """Lookup table for in game items"""
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r})"

def create_item(id, name):
        with Session(engine) as session:
            item = Item(id = id, name = name)
        session.add(item)
        session.commit()

def read_item():
    pass

def update_item():
    pass

def delete_item():
    pass

# Inventory
class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    character_id = mapped_column(ForeignKey("character.id"))

    def __repr__(self) -> str:
        return f"Inventory(id={self.id!r}, entity_id={self.entity_id!r})"
    
def create_inventory(id, entity_id):
        with Session(engine) as session:
            inventory = Inventory(id = id, entity_id = entity_id)
        session.add(inventory)
        session.commit()

def read_inventory():
    pass

def update_inventory():
    pass

def delete_inventory():
    pass

# Inventory-Item
class InventoryItem(Base):
    """Junction table between inventories and items"""
    __tablename__ = "inventory_item"
    inventory_id = mapped_column(ForeignKey("inventory.id"), primary_key=True)
    item_id = mapped_column(ForeignKey("item.id"), primary_key=True)
    count: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"IntentoryItem(inventory_id={self.inventory_id!r}, item_id={self.item_id!r}, count={self.count!r})"

def create_inventory_item(inventory_id, item_id):
        with Session(engine) as session:
            inventory_item = InventoryItem(id = id, inventory_id = inventory_id, item_id = item_id)
        session.add(inventory_item)
        session.commit()

def read_inventory_item():
    pass

def update_inventory_item():
    pass

def delete_inventory_item():
    pass

# Equipment
class Equipment(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(256))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    def __repr__(self) -> str:
        return f"Equipment(id={self.id!r}, name={self.name!r}, description={self.description!r})"
    
# Dungeon
class Dungeon(Base):
    __tablename__ = "dungeon"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    settings_id: Mapped[int] = mapped_column(ForeignKey("settings.id"))
  

    def __repr__(self) -> str:
        return f"Dungeon(id={self.id!r}, settings_id={self.settings_id!r})"

#Level
class Level(Base):
    __tablename__ = "level"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    dungeon_id: Mapped[int] = mapped_column(ForeignKey("dungeon.id"))

    def __repr__(self) -> str:
        return f"Dungeon(id={self.id!r}, dungeon_id={self.dungeon_id!r})"


# Room-Wall
class RoomWall(Base):
    """Static table to help with wall naming/pairing"""
    __tablename__ = "room_wall"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    side: Mapped[str] = mapped_column(String(5)) # north, east, south, west
    pair: Mapped[int] = mapped_column()        
        
    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, side={self.side!r}, pair={self.pair!r})"

def create_room_walls():
    """Hardcoded room_wall values"""
    with Session(engine) as session:
        north = RoomWall(id = 0, side = "north", pair = 2)
        east = RoomWall(id = 1, side = "east", pair = 3)
        south = RoomWall(id = 2, side = "south", pair = 0)
        west = RoomWall(id = 3, side = "west", pair = 1)
    session.add_all([north, east, south, west])
    session.commit()

def read_room_walls():
    '''
    walls = []
    with Session(db.engine) as session:
        stmt = select(RoomWall).distinct()
    return session.execute(stmt)
    '''
    pass

def update_room_walls():
    pass

def delete_room_walls():
    pass

# TODO: Refactor this into Tile class
# DungeonTile
class Tile(Base):
    """Tile class"""
    __tablename__ = "tile"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    sprite_id: Mapped[int] = mapped_column(ForeignKey("sprite.id"))
    tile_type_id: Mapped[int] = mapped_column(ForeignKey("tile_type.id"))
    treasure_id: Mapped[int] = mapped_column(ForeignKey("treasure.id"))

    def __repr__(self) -> str:
        return f"Tile(id={self.id!r}, room_id={self.room_id!r})"

def create_tile(id, room_id):
    """Insert new tile with arguments"""
    with Session(engine) as session:
        tile = Tile(id = id, room_id = room_id)
    session.add(tile)
    session.commit()

def read_tile():
    pass

def update_tile():
    pass

def delete_tile():
    pass

# TileType
class TileType(Base):
    # TODO name, description, can_be_occupied, sprite_id
    __tablename__ = "tile_type"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(256))
    can_be_occupied: Mapped[Boolean] = mapped_column(Boolean)
    #sprite_id: Mapped[int] = mapped_column(ForeignKey("sprite.id"))
    
    def __repr__(self) -> str:
        return f"TileType(id={self.id!r}, name={self.name!r}, description={self.description!r})"



# Treasure
class Treasure(Base):
    # TODO tile_id
    __tablename__ = "treasure"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), nullable=True)
    
    def __repr__(self) -> str:
        return f"TileType(id={self.id!r}, tile_id={self.tile_id!r})"

# Room
class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO rename this (they should reflect level grid pos_x/y)
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()
    level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, x={self.x!r}, y={self.y!r})"
    
def create_room(id, x, y):
    with Session(engine) as session:
        room = Room(id = id, x = x, y = y)
    session.add(room)
    session.commit()

def read_room():
    pass

def update_room():
    pass

def delete_room():
    pass

# Door
class Door(Base):
    __tablename__ = "door"
    id: Mapped[int] = mapped_column(primary_key=True)
    # room_id = The room to which the door leads
    room_id: Mapped[int] = mapped_column() 

    def __repr__(self) -> str:
        return f"Door(id={self.id!r}, room_id={self.room_id!r})"

def create_door(id, room_id):
    with Session(engine) as session:
        door = Door(id=id, room_id = room_id)
    session.add(door)
    session.commit()

def read_door():
    pass

def update_door():
    pass

def delete_door():
    pass

# Room-Door
class RoomDoor(Base):
    __tablename__ = "room_door"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_wall_id: Mapped[int] = mapped_column() # TODO: make this second PK
    door_id: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"RoomDoor(id={self.id!r}, room_wall_id={self.room_wall_id!r}, door_id={self.door_id!r})"

def create_room_door(id, room_wall_id, door_id):
    with Session(engine) as session:
        room_door = RoomDoor(id=id, room_id = room_wall_id, door_id = door_id)
    session.add(room_door)
    session.commit()

def read_room_door():
    pass

def update_room_door():
    pass

def delete_room_door():
    pass


# Testing stuff
def main() -> None:
    Base.metadata.create_all(engine)
    create_item(id=0, name="Robe")
    create_item(id=1, name="Wizard Hat") 


if __name__ == "__main__":
    main()