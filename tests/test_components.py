import pytest
from copd.engine.components import *


def test_create_position():
    pos = Position(2, 3)
    assert (pos.x, pos.y) == (2, 3)


def test_create_velocity():
    vel = Velocity(1, 0)
    assert (vel.dx, vel.dy) == (1, 0)


def test_position_plus_velocity():
    pos = Position(2, 3)
    vel = Velocity(1, 0)
    pos = pos + vel

    assert (pos.x, pos.y) == (3, 3)
