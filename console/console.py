# -*- coding: utf-8 -*-
import curses
import locale

class Color(object):
  def __init__(self, color, attr):
    self._color = color
    self._attr = attr

  @property
  def color(self):
    return self._color

  @property
  def attr(self):
    return self._attr

class ColorTable(object):
  Colors = {
      "black" : Color(curses.COLOR_BLACK, 0),
      "red" : Color(curses.COLOR_RED, 0),
      "cyan" : Color(curses.COLOR_CYAN, 0),
      "blue" : Color(curses.COLOR_BLUE, 0),
      "green" : Color(curses.COLOR_GREEN, 0),
      "white" : Color(curses.COLOR_WHITE, 0),
      "yellow" : Color(curses.COLOR_YELLOW, 0),
      "magenta" : Color(curses.COLOR_MAGENTA, 0),
      "light black" : Color(curses.COLOR_BLACK, curses.A_BOLD),
      "light red" : Color(curses.COLOR_RED, curses.A_BOLD),
      "light cyan" : Color(curses.COLOR_CYAN, curses.A_BOLD),
      "light blue" : Color(curses.COLOR_BLUE, curses.A_BOLD),
      "light green" : Color(curses.COLOR_GREEN, curses.A_BOLD),
      "light white" : Color(curses.COLOR_WHITE, curses.A_BOLD),
      "light yellow" : Color(curses.COLOR_YELLOW, curses.A_BOLD),
      "light magenta" : Color(curses.COLOR_MAGENTA, curses.A_BOLD),
      }

  def __init__(self):
    self._chache = dict()
    self._color_id = dict()

  def id(self, fg, bg="black"):
    color_pair = (fg, bg)
    if color_pair in self._chache:
      return self._chache[color_pair];
    if color_pair not in self._color_id:
      self._color_id[color_pair] = len(self._color_id) + 1
      curses.init_pair(self._color_id[color_pair], self.Colors[fg].color, self.Colors[bg].color)
    color_id = self._color_id[color_pair]
    color_pair_id = curses.color_pair(color_id)
    self._chache[color_pair] = color_pair_id | self.Colors[fg].attr | self.Colors[bg].attr;
    return self._chache[color_pair]

class Screen(object):
  def __init__(self, screen):
    self._screen = screen
    self._colors = ColorTable()

  def move(self, coord):
    self._screen.move(coord.y, coord.x)
    return self

  def write(self, string, fg="white", bg="black"):
    self._screen.addstr(string, self._colors.id(fg, bg))
    return self

  def clear(self):
    self._screen.clear()
    return self

  def refresh(self):
    self._screen.refresh()

class Console(object):
  def __init__(self, application):
    self._application = application
    self._console = curses.initscr()

  def run(self):
    self._initialize()
    curses.wrapper(self._main_loop)

  def _initialize(self):
    locale.setlocale(locale.LC_ALL, '')
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    self._console.keypad(True)

  def _main_loop(self, args):
    screen = Screen(self._console)
    self._application.initialize(screen)
    while True:
      self._application.update(screen, self._read_key())

  def _read_key(self):
    self._console.refresh()
    return chr(self._console.getch())
