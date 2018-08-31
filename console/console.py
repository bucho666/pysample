# -*- coding: utf-8 -*-
import curses
import locale

class Color(object):
  BLACK         = (curses.COLOR_BLACK, 0)
  RED           = (curses.COLOR_RED, 0)
  CYAN          = (curses.COLOR_CYAN, 0)
  BLUE          = (curses.COLOR_BLUE, 0)
  GREEN         = (curses.COLOR_GREEN, 0)
  WHITE         = (curses.COLOR_WHITE, 0)
  YELLOW        = (curses.COLOR_YELLOW, 0)
  MAGENTA       = (curses.COLOR_MAGENTA, 0)
  LIGHT_BLACK   = (curses.COLOR_BLACK, 0)
  LIGHT_RED     = (curses.COLOR_RED, curses.A_BOLD)
  LIGHT_CYAN    = (curses.COLOR_CYAN, curses.A_BOLD)
  LIGHT_BLUE    = (curses.COLOR_BLUE, curses.A_BOLD)
  LIGHT_GREEN   = (curses.COLOR_GREEN, curses.A_BOLD)
  LIGHT_WHITE   = (curses.COLOR_WHITE, curses.A_BOLD)
  LIGHT_YELLOW  = (curses.COLOR_YELLOW, curses.A_BOLD)
  LIGHT_MAGENTA = (curses.COLOR_MAGENTA, curses.A_BOLD)
  LIST = (BLACK, RED , CYAN, BLUE,
          GREEN, WHITE, YELLOW, MAGENTA,
          LIGHT_BLACK, LIGHT_RED, LIGHT_CYAN, LIGHT_BLUE,
          LIGHT_GREEN, LIGHT_WHITE, LIGHT_YELLOW, LIGHT_MAGENTA)

class ColorTable(object):
  def __init__(self):
    self._attrCache = dict()
    self._colorCache = dict()

  def id(self, fg, bg=Color.BLACK):
    color_pair = (fg, bg)
    if color_pair not in self._attrCache:
      self.registAttr(color_pair)
    return self._attrCache[color_pair];

  def registAttr(self, attr_pair):
    ((fg_color, fg_attr), (bg_color, bg_attr)) = attr_pair
    color_pair = (fg_color, bg_color)
    if color_pair not in self._colorCache:
      self.registColor(fg_color, bg_color)
    self._attrCache[attr_pair] = self._colorCache[color_pair] | fg_attr | bg_attr

  def registColor(self, fg, bg):
    color_id = len(self._colorCache) + 1
    curses.init_pair(color_id, fg, bg)
    self._colorCache[(fg, bg)] = curses.color_pair(color_id)

class Console(object):
  def __init__(self):
    self._console = curses.initscr()
    self._colors = None
    self._initialize()

  def nonBlocking(self):
    self._console.nodelay(True)
    return self

  def colorOn(self):
    if curses.has_colors():
      curses.start_color()
      self._colors = ColorTable()
      self._noColor = ColorTable()
    return self

  def run(self, func):
    curses.wrapper(func)

  def move(self, coord):
    self._console.move(coord.y, coord.x)
    return self

  def write(self, string, fg=Color.WHITE, bg=Color.BLACK):
    self._console.addstr(string, self._colors.id(fg, bg) if self._colors else 0)
    return self

  def clear(self):
    self._console.clear()
    return self

  def refresh(self):
    self._console.refresh()

  def getKey(self):
    key = self._console.getch()
    if key is -1: return None
    return chr(key)

  def sleep(self, msec):
    curses.napms(msec)

  def _initialize(self):
    locale.setlocale(locale.LC_ALL, '')
    curses.noecho()
    curses.cbreak()
    self._console.keypad(True)
