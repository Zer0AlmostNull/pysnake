# PYSnake

Thats fairy simple snake like game coded in python. With graphical interface made with pygame.

## simple API

It's all that simple to implement own python snake game.
```python3

map_width, map_height = 15, 15


game = GameGraphical(
    arena_size = (width, height),
    cell_size = 25)

```

To 'tick' the game you just call a:
```python3
direction = Direction.UP

game.tick(direction)
```

where direction is an enum object

```python3
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
```

In order to draw the game on to the pygame screen object use:
```python3
game_offset = (0, 0)

game.draw(screen, game_offset)
```

You also have an example of the game implementation in 
[a relative link](/main.py)
    
