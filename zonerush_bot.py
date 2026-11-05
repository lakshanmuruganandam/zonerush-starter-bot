"""
ZONE RUSH: bot template (strategy round)
========================================

This file is the ONLY thing we give every team. It contains no strategy.
Uploaded as it is, it plays a valid game but does nothing: it stays at home every turn.
Your job is to write the strategy inside act().

------------------------------------------------------------------------------
FIXED: DO NOT CHANGE
------------------------------------------------------------------------------
  1. The file must define a function named exactly:   act(state)
  2. act() receives ONE argument, `state` (a dict, described below).
  3. act() must return ONE of these strings:
         "NORTH"  "EAST"  "SOUTH"  "WEST"  "STAY"  "SHIELD"
  4. Python standard library only (no numpy, no pip packages, no files, no internet).
  5. Time limit: 200 ms per turn (2 s on the first turn).
  6. If act() crashes, runs too long, or returns an action that is not in
     state["legal_actions"], your bot plays "STAY" for that turn.
  7. print() output goes to your bot's log on the website, not into the game.

------------------------------------------------------------------------------
INPUT: what `state` contains
------------------------------------------------------------------------------
Coordinates are [x, y]: x = column, y = row, [0, 0] = top-left corner.

  state["turn"]              current turn number (starts at 0)
  state["turns_remaining"]   turns left, including this one
  state["turns"]             total turns in the game (80)
  state["width"]             board width  (8)
  state["height"]            board height (8)
  state["walls"]             list of [x, y] cells nobody can enter (may be empty)

  state["owner"][y][x]       -1 = neutral, otherwise the id (0-3) of the owner
  state["value"][y][x]       points per turn the cell is worth
  state["level"][y][x]       2 = upgraded (counts double), 1 = normal, 0 = unowned

  state["priority_seat"]     id of the bot that wins a tie for an empty cell this turn
  state["legal_actions"]     list of the actions you may return RIGHT NOW
  state["rules"]             the rule numbers (capture, upgrade, steal, cooldown,
                             stun, raid_bonus, backfire, ...)

  state["self"]              your own bot (same fields as below)
  state["bots"]              list of all 4 bots, indexed by id; each one has:
      "id"         0-3
      "position"   [x, y] where it stands
      "home"       [x, y] its home corner
      "progress"   turns it has already stayed on its current cell
      "need"       stays its current cell needs in total (0 = nothing to do there)
      "score"      points so far
      "income"     points per turn it earns right now
      "cells"      number of cells it owns
      "cooldown"   {"SHIELD": k}, turns until it can shield again (0 = ready)
      "shield"     not None while its shield is up
      "frozen"     turns it is still frozen (0 = free)

------------------------------------------------------------------------------
OUTPUT: what act() returns
------------------------------------------------------------------------------
  "NORTH" / "EAST" / "SOUTH" / "WEST"   move one cell (y-1 / x+1 / y+1 / x-1)
  "STAY"                                stay on your cell (to take or upgrade it)
  "SHIELD"                              raise your shield this turn

Full game rules: see README.md in this repository, or the Rules page on the arena.
"""

# You may import anything from the Python standard library, for example:
# import random
# from collections import deque


def act(state):
    """Called once per turn. Return one action string (see OUTPUT above)."""

    # ------------------------------------------------------------------
    # YOUR STRATEGY GOES HERE.
    # Read `state`, decide, and return one of the strings in
    # state["legal_actions"].
    # ------------------------------------------------------------------

    return "STAY"
