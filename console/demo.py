# -*- coding: utf-8 -*-
import random
from console import Console
from console import Color


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
    self._console = Console().colorOn().nonBlocking()

  def run(self):
    self.render()
    interval = int(1000/30)
    while True:
      self.update()
      self._console.sleep(interval)

  def update(self):
    key = self._console.getKey()
    self._coord += Walk.KeyMap.get(key, Coord(0, 0))
    self.render()

  def render(self):
    self._console.clear()
    self._console.move(Coord(1, 2)).write("+", Color.LIGHT_YELLOW)
    self._console.move(Coord(3, 4)).write("T", Color.GREEN, Color.BLUE)
    self._console.move(Coord(5, 6)).write("*", Color.LIGHT_YELLOW, Color.GREEN)
    self._console.move(Coord(7, 8)).write("&", random.choice(list(Color.LIST)))
    self._console.move(self._coord).write("@", Color.LIGHT_YELLOW).move(self._coord)

if __name__ == '__main__':
  Walk().run()
