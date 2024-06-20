"""Create and configure a local SQLite database"""

import sqlalchemy
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import select, update, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Session


engine = create_engine("sqlite://", echo=True)

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
        game_entity = GameEntity(id=id, name=name)
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
        item = Item(id=id, name=name)
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
        inventory = Inventory(id=id, entity_id=entity_id)
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
        inventory_item = InventoryItem(
            id=id, inventory_id=inventory_id, item_id=item_id
        )
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


# Level
class Level(Base):
    __tablename__ = "level"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    dungeon_id: Mapped[int] = mapped_column(ForeignKey("dungeon.id"))

    def __repr__(self) -> str:
        return f"Dungeon(id={self.id!r}, dungeon_id={self.dungeon_id!r})"


# Wall
class Wall(Base):
    """Static table to help with wall naming/pairing"""

    __tablename__ = "wall"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    side: Mapped[str] = mapped_column(String(5))  # north, east, south, west
    pair: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"RoomWall(id={self.id!r}, side={self.side!r}, pair={self.pair!r})"





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
        tile = Tile(id=id, room_id=room_id)
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
    # sprite_id: Mapped[int] = mapped_column(ForeignKey("sprite.id"))

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
    #level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, x={self.x!r}, y={self.y!r})"

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

def update_room():
    pass


def delete_room():
    pass


# Door
class Door(Base):
    __tablename__ = "door"
    id: Mapped[int] = mapped_column(primary_key=True)
    # room_id = The room to which the door leads
    room_id: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Door(id={self.id!r}, room_id={self.room_id!r})"







def delete_door():
    pass


# Room-Door (with wall!)
class RoomWallDoor(Base):
    __tablename__ = "room_wall_door"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id = mapped_column(ForeignKey("room.id"))
    wall_id: Mapped[int] = mapped_column(ForeignKey("wall.id"))  # TODO: make this second PK
    door_id: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"RoomDoor(id={self.id!r}, wall_id={self.wall_id!r}, door_id={self.door_id!r})"


def update_room_wall_door():
    pass


def delete_room_wall_door():
    pass


# TODO move your CRUD methods here when you're done with them
class DB:
    def __init__(self):
        #self.create_walls()
        pass

    Base.metadata.create_all(engine)

    def create_walls(self):
        """Hardcoded wall values"""
        with Session(engine) as session:
            north = Wall(id=0, side="north", pair=2)
            east = Wall(id=1, side="east", pair=3)
            south = Wall(id=2, side="south", pair=0)
            west = Wall(id=3, side="west", pair=1)
        session.add_all([north, east, south, west])
        session.commit()


    def read_wall(self, id):
        stmt = select(Wall).where(Wall.id == id)
        with Session(engine) as session:
            wall = session.execute(stmt).first()
        return wall
    
    def get_opposite_wall(self, wall_id):
        stmt = select(Wall.pair).where(Wall.id == wall_id)
        with Session(engine) as session:
            pair = session.execute(stmt).first()
        return pair[0]


    def create_room(self, id, x, y):
        with Session(engine) as session:
            room = Room(id=id, x=x, y=y)
        session.add(room)
        session.commit()
        return room.id

    def read_room(self, id=0):
        stmt = select(Room.x, Room.y).where(Room.id == id)
        with Session(engine) as session:
            result = session.execute(stmt).one_or_none()
            # room = {
            #     "id": id,
            #     "x": result[0],
            #     "y": result[1]
            # }
        return result
    
    def get_room_if_exists(self, x, y, wall_pair):
        match (wall_pair): # same switch exists on api.py
            # facing....
            case 0: # north
                y -= 1
            case 1: # east
                x += 1
            case 2: # south
                y += 1
            case 3: # west
                x -= 1
        stmt = select(Room.id).where((Room.x == x) & (Room.y == y))
        with Session(engine) as session:
            room = session.execute(stmt).one_or_none()
        if room is None:
            return 0
        else:
            return room[0]

    def get_rooms(self):
        stmt = select(Room)
        rooms = []
        with Session(engine) as session:
            for row in session.execute(stmt):
                #print(row)
                rooms.append(row)
        return rooms

    def create_door(self, room_id=None):
        with Session(engine) as session:
            door = Door(room_id=room_id)
        session.add(door)
        session.commit()
        return door.id


    def read_door(self, id):
        stmt = select(Door).where(Door.id == id)
        with Session(engine) as session:
            door = session.scalars(stmt).first()
        return door


    def create_room_wall_door(self, room_id, wall_id, door_id=None):
        with Session(engine) as session:
            room_wall_door = RoomWallDoor(room_id=room_id, wall_id=wall_id, door_id=door_id)
        session.add(room_wall_door)
        session.commit()
        return room_wall_door.id

    def read_room_wall_door(self, id=0):
        stmt = select(RoomWallDoor).where(RoomWallDoor.id == id)
        with Session(engine) as session:
            rwd = session.execute(stmt).first()
        return rwd
    
    def get_door_from_rwd(self, room_id, wall_pair):
        stmt = select(RoomWallDoor).where(
            (RoomWallDoor.room_id == room_id) &
            (RoomWallDoor.wall_id == wall_pair)
            )
        with Session(engine) as session:
            door = session.execute(stmt).first()
        return door
    
    def get_room_from_door(self, door_id):
        stmt = select(RoomWallDoor.room_id).where(
            RoomWallDoor.door_id == door_id
        )
        with Session(engine) as session:
            room = session.execute(stmt).first()
            print(room)
        return room[0]
    
    def get_wall_from_door(self, door_id):
        stmt = select(RoomWallDoor.wall_id).where(
            RoomWallDoor.door_id == door_id
        )
        with Session(engine) as session:
            wall = session.execute(stmt).first()
        return wall[0]
    
    def add_rwd_door_from_room(self, room_id, wall, door_id):
        stmt = (
            update(RoomWallDoor)
            .where(
                (RoomWallDoor.room_id == room_id) &
                (RoomWallDoor.wall_id == wall)
            )
            .values(door_id=door_id)
        )
        with Session(engine) as session:
            rwd = session.execute(stmt)
        return rwd

    #def add_rwds_for_room(seld, room_id):

    def get_room_count(self):
        stmt = select(func.count()).select_from(Room)
        with Session(engine) as session:
            room_count:int = session.execute(stmt).scalar()
        return room_count
        
    def update_door(self, door_id, room_id):
        stmt = (
            update(Door).where(
                (Door.id == door_id)
            )
            .values(room_id=room_id)
        )
        with Session(engine) as session:
            door = session.execute(stmt)
        return door
    
    def get_rwds(self):
        stmt = select(RoomWallDoor)
        rooms = []
        with Session(engine) as session:
            for row in session.execute(stmt):
                #print(row)
                rooms.append(row)
        return rooms

    def get_xy_from_room(self, room_id):
        room = self.read_room(room_id)
        print(f"room = {room}")
        if room is None:
            return {'x':999, 'y':999}
        room_dict = {
            "x":room.x,
            "y":room.y
        }
        print(room_dict)
        return room_dict
        

# Testing stuff
def main() -> None:
    Base.metadata.create_all(engine)
    create_item(id=0, name="Robe")
    create_item(id=1, name="Wizard Hat")
    test_db = DB()
    test_db.create_room(0, 1, 2)
    test_db.get_xy_from_room(0)

if __name__ == "__main__":
    main()
