# PYSnake

That's a fairly simple snake like game coded in python. With graphical interface made using pygame.

## A simple API

It's all that simple to implement own python snake game.
```python3

map_width, map_height = 15, 15


game = SnakeWindowed(
    arena_size = (width, height),
    cell_size = 25)

```

To 'tick' the game you just call a:
```python3
direction = Direction.UP

game.tick(direction)
```

where direction is a predefined point object

```python3
class Direction:
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
```

In order to draw the game on to the pygame screen object use:
```python3
game_offset = (0, 0)

game.draw(screen, game_offset)
```

You also have an example of the game implementation [here](/main.py).

## Files description

[game.py](/game.py) - it'a a implementation of main snake-game classes
```python3
SnakeWindowed
SnakeBasic
```
[point.py](/point.py) - contains a definition of ```Point``` class
[subconsole.py](/subconsole.py) - really weird definition of class ```console``` class
[color_settings.py](/color_settings.py) - contains hardcoded snake color palette used in ```GameGraphical``` class

--------------
[example/main.py](/example/main.py) - actual snake game implementation\
[example/game_settings.py](/example/game_settings.py) - contains settings for the implementation\
[example/game_state.py](/example/game_state.py) - contains games states of the implementation\
[example/ui.py](/example/ui.py) - contains ```UIElement``` python-pygame class for UI

---------------------
So, If you need to get only snake game API copy to your project's folder following files/folders:\
[color_settings.py](/color_settings.py), [game.py](/game.py), [assets](/assets)

GLHF ^-^




