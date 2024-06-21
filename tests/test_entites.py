import pytest
from copd.engine.entities import Entity
from copd.engine.components import Position, Velocity

def test_add_component(game):
    entity = Entity(game,0,0,name="player")
    position = Position(0, 0)
    entity.add_component(position)
    assert entity.get(Position) == position

# def test_update(game):
#     entity = Entity(game,0, 0, name="player")
#     entity.moving = True
#     entity.x_dest = 10
#     entity.y_dest = 10
#     entity.update()
#     assert entity.x == 10
#     assert entity.y == 10

# def test_animate():
#     entity = Entity(0, 0, None)
#     entity.x_dest = 10
#     entity.y_dest = 10
#     dx, dy = entity.animate()
#     assert dx == 1
#     assert dy == 1

#     entity.x_dest = 0
#     entity.y_dest = 10
#     dx, dy = entity.animate()
#     assert dx == -1
#     assert dy == 1

#     entity.x_dest = 0
#     entity.y_dest = 0
#     dx, dy = entity.animate()
#     assert dx == 0
#     assert dy == 0

#     entity.x_dest = 10
#     entity.y_dest = 0
#     dx, dy = entity.animate()
#     assert dx == 1
#     assert dy == -1