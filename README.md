# Zone Rush: StrategyBot Starter

The official starter template for the **Zone Rush** strategy round of StrategyBot.

You write one Python function, `act(state)`. Every turn it receives the whole board and returns one move. Your bot fights three others for territory on an 8×8 board for 80 turns, and the arena ranks every bot by rating.

> `zonerush_bot.py` contains **no strategy**. Uploaded as it is, it plays a valid game but stays at home every turn and finishes last. The strategy is yours to write.

---

## Quick start

1. Download [`zonerush_bot.py`](zonerush_bot.py).
2. Write your strategy inside `act(state)`.
3. Sign up on the arena with the invite code you were given, then upload the file under **My bots**.
4. Your bot plays 1 check game, then 12 placement games, then joins the ranked ladder.

Arena: **https://strategybot-arena.vercel.app/zonerush/**

---

## The contract (fixed: the same for every team)

| | |
|---|---|
| File | One `.py` file |
| Function | `act(state)`, with exactly this name and one argument |
| Returns | One of `"NORTH"`, `"EAST"`, `"SOUTH"`, `"WEST"`, `"STAY"`, `"SHIELD"` |
| Libraries | Python 3 standard library only. Packages from pip, such as numpy, are not available. |
| Time | 200 ms per turn, or 2 s on the first turn |
| Mistakes | A crash, a late answer, or an action not in `state["legal_actions"]` plays `"STAY"` for that turn |
| Debugging | `print()` output goes to your bot's log on the arena, not into the game |
| Memory | The bot is loaded fresh for every match. Global variables survive between the turns of one match only. |

### Limits

| Limit | Value |
|---|---|
| Bot file size | 200 KB |
| Time per turn | 200 ms (first turn 2 s) |
| Start-up time | 5 s |
| CPU time per match | 60 s in total |
| Memory | 512 MB |
| Log output | 1 MB per match |

**Not allowed:**
- network access;
- reading or writing files;
- starting other processes (`subprocess`, `os.system`, `multiprocessing`);
- `ctypes`.

---

## Input: `state`

Coordinates are `[x, y]`: x is the column, y is the row, and `[0, 0]` is the top-left corner.

| Field | Meaning |
|---|---|
| `turn` | Current turn number, starting at 0 |
| `turns_remaining` | Turns left, including this one |
| `turns` | Total turns in the game (80) |
| `width`, `height` | Board size (8 × 8) |
| `walls` | List of `[x, y]` cells nobody can enter (may be empty) |
| `owner[y][x]` | `-1` = neutral, otherwise the id (0–3) of the owner |
| `value[y][x]` | Points per turn the cell is worth |
| `level[y][x]` | `2` = upgraded (counts double), `1` = normal, `0` = unowned |
| `priority_seat` | Id of the bot that wins a tie for an empty cell this turn |
| `legal_actions` | The actions you may return **right now** |
| `rules` | The rule numbers (`capture`, `upgrade`, `steal`, `cooldown`, `stun`, `raid_bonus`, `backfire`, ...) |
| `self` | Your own bot (same fields as below) |
| `bots` | All 4 bots, indexed by id |

Each bot in `bots` (and `self`) has:

| Field | Meaning |
|---|---|
| `id` | 0–3 |
| `position` | `[x, y]` where it stands |
| `home` | `[x, y]` of its home corner |
| `progress` | Turns it has already stayed on its current cell |
| `need` | Stays its current cell needs in total (`0` = nothing to do there) |
| `score` | Points so far |
| `income` | Points per turn it earns right now |
| `cells` | Number of cells it owns |
| `cooldown` | `{"SHIELD": k}`: turns until it can Shield again (`0` = ready) |
| `shield` | Not `None` while its Shield is up |
| `frozen` | Turns it is still frozen (`0` = free) |

## Output: one action

| Action | Effect |
|---|---|
| `"NORTH"` / `"EAST"` / `"SOUTH"` / `"WEST"` | Move one cell (y−1 / x+1 / y+1 / x−1) |
| `"STAY"` | Stay on your cell (to take it or upgrade it) |
| `"SHIELD"` | Raise your Shield this turn |

---

## Official rules

### 1. Setup
1. **Board:** 8×8 cells. Each cell is worth 1, 2 or 3 points per turn, generally higher toward the middle. Every map is mirrored, so all four corners are equal.
2. **Players:** 4 bots, one per corner. Your corner is your **home**: you always own it and it can never be taken.
3. **Length:** 80 turns. All other cells start neutral.

### 2. Each turn
4. All 4 bots choose an action at the same time: **North, East, South, West, Stay** or **Shield**.
5. The turn is resolved in this order:
   1. Moves and Shields.
   2. Takes, upgrades and freezes.
   3. Scoring.
   4. The priority token passes to the next seat.

### 3. Movement
6. You move one cell (no diagonals) or stay where you are.
7. A cell with a bot on it at the start of the turn is **closed**. You can't enter it, even if that bot is leaving, so bots can't swap places.
8. If two or more bots move into the same empty cell:
   - the cell's **owner** gets it;
   - otherwise the bot closest to the **priority token**, in seat order, gets it;
   - the others stay put.
9. A blocked move counts as **Stay**.

### 4. Taking cells
10. Stay on a cell that isn't yours and it becomes yours, at level 1:
    - a neutral cell takes **1 turn**;
    - a rival's level-1 cell takes **1 turn**;
    - a rival's **upgraded** cell takes **3 turns**.
11. **Raid bonus:** taking a **rival's** cell, not a neutral one, pays a one-off **8 × the cell's value × its level** points.
12. Moving off a cell, shielding or being frozen resets your progress on it to zero.

### 5. Upgrading
13. Stay **3 turns** on your own cell to upgrade it. It now counts **double**.
14. A taken cell always drops back to level 1.

### 6. Shield
15. Instead of moving, you may **Shield**. For that turn:
    - none of your cells can be taken;
    - every rival **staying** on your land, including your home, loses its progress and is **frozen for 2 turns**.
16. **Frozen** means the bot can only Stay. Its chosen action is ignored.
17. **Backfire:** a Shield that catches nobody freezes **you** for 2 turns. A rival who is already frozen can't be caught again, so a Shield that only reaches frozen rivals still backfires.
18. **Cooldown:** after a Shield you can't Shield again for the next **4 turns**. A Shield turn doesn't count as staying, so you make no take or upgrade progress that turn.

### 7. Scoring and winning
19. At the end of every turn, each bot scores the value of every cell it owns, ×2 for upgraded cells.
20. After 80 turns, the highest total wins. Places run 1st to 4th, and equal totals share a place.
21. Nobody is ever knocked out.

### 8. Your bot
22. Your bot is one Python file with `act(state)`, standard library only. `state` shows the whole board and all four bots, and `legal_actions` lists the moves you may make.
23. You get **200 ms** per turn, or 2 s on the first turn. A bot that crashes, is late or returns an illegal action plays **Stay**.
24. **Ladder:** a new bot plays 1 test game, then 12 placement games, then ranked games. Finishing above a bot raises your rating; finishing below it lowers it.

### 9. Arena day (robots)
25. The server runs the game, and its board is **official**. Robots only act out the moves.
26. Robot LEDs show the team colour, turn **blue** when shielding and **flash** when frozen. The big screen shows the live board, scores and events.

---

## FAQ

**Can I use extra functions, classes or imports?**
Yes. Anything works as long as the file defines `act(state)` and uses only the standard library.

**Can my bot remember things between turns?**
Yes, within one match: use global variables. Each match starts with a fresh copy of your bot.

**What if my code has a syntax error?**
The upload is rejected and the arena shows you the error.

**What if my bot crashes during a turn?**
It plays `"STAY"` that turn and the game goes on. Check your bot's log on the arena.
