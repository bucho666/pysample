# -*- coding: utf-8 -*-
from console import Console

class Coord(object):
  def __init__(self, x, y):
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  def __add__(self, other):
    return Coord(self.x + other.x, self.y + other.y)

class Walk(object):
  KeyMap = {
    "h": Coord(-1,  0), "j": Coord(0,  1), "k": Coord(0, -1), "l": Coord(1, 0),
    "y": Coord(-1, -1), "u": Coord(1, -1), "b": Coord(-1, 1), "n": Coord(1, 1)
  }

  def __init__(self):
    self._coord = Coord(1, 1)

  def initialize(self, screen):
    self.render(screen)

  def update(self, screen, key):
    self._coord += Walk.KeyMap.get(key, Coord(0, 0))
    self.render(screen)

  def render(self, screen):
    screen.clear()
    screen.move(Coord(1, 2)).write("+", "light yellow")
    screen.move(Coord(3, 4)).write("T", "green", "blue")
    screen.move(Coord(5, 6)).write("*", "light yellow", "green")
    screen.move(self._coord).write("@", "white").move(self._coord)

if __name__ == '__main__':
  Console(Walk()).run()
