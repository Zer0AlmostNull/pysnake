from random import choice
from point import Point


class SnakeBasic():
    '''
    Contains basic implementation of snake game
    '''
    def __init__(self, arena_size: tuple = (15, 15)):
        self.arena_dimensions = arena_size
        
        # set deafult
        self.reset()
        
    def reset(self):
        # x, y 
        self.free_spaces = [Point(x, y) for y in range(0, self.arena_dimensions[1]) for x in range(0, self.arena_dimensions[0])]
        
        # set snake default direction
        self.snake_direction = Direction.UP
        
        # center snake's position
        self.snake_head_pos = Point(self.arena_dimensions[0]//2, self.arena_dimensions[1]//2)
        self.free_spaces.remove(self.snake_head_pos)
        
        # add head position to body position
        self.snake_body_pos = [self.snake_head_pos.copy()]
        
        # allocate area with snake's blocks
        for pos in self.snake_body_pos[1:]:
            self.free_spaces.remove(pos)
        
        #
        self.score = 0
        #
        self.place_apple()
        
        # handle death
        self.died = False

    def place_apple(self):
        # random pick random apple position    
        self.apple_pos = choice(self.free_spaces)
        self.free_spaces.remove(self.apple_pos)
        
    def tick(self, _input):
        '''
        Updates the game
        
        returns: (game_over: bool, score: int)
        '''
        
        # return if snake already died 
        if self.died:
            return (0, self.died, self.score)
        
        # parse the int input
        if(isinstance(_input, int)):
            self.snake_direction = Direction.directions[_input]
        else:
            # input
            self.snake_direction = _input
        
        # check if snake out of border
        # or ran into itself
        if self.is_collision(self.snake_head_pos + self.snake_direction):
            self.died = True
            return (True, self.score)

        # move snake's head 
        self.snake_head_pos += self.snake_direction
        
        # check if ate an apple
        if self.snake_head_pos == self.apple_pos:
            # add score
            self.score += 1
            
            # add a block to the snake 
            self.snake_body_pos.insert(0, self.snake_head_pos)
            
            # pick apple random position and del it from free spaces
            self.place_apple()
            
            return (False, self.score)
        else:
            # add tail position to free spaces 
            self.free_spaces.append(self.snake_body_pos[-1])
            
            # remove head pos from free spaces
            self.free_spaces.remove(self.snake_head_pos)
            
            # move the rest of the snake's body
            for i in range(len(self.snake_body_pos) - 1, 0, -1):
                # move block
                self.snake_body_pos[i] = self.snake_body_pos[i-1]                    
            # move head
            self.snake_body_pos[0] = self.snake_head_pos
        

        return (False, self.score)

    def is_collision(self, point: Point):
        # check if out of map
        if (point.x >= self.arena_dimensions[0] or point.x < 0 or\
            point.y >= self.arena_dimensions[1] or point.y < 0):
            return True

        # check for collision with snake
        if(point in self.snake_body_pos[:-1] or\
            point == self.snake_head_pos):
            return True
        
        # 
        if len(self.snake_body_pos) == 2 and\
            point == self.snake_body_pos[-1]:
            return True
        
        return False
    
    def _get_matrix(self):
        matrix = [[ObjectsCodes.VOID for y in range(0, self.arena_dimensions[1])] for x in range(0, self.arena_dimensions[0])]
        
        # allocate snake body
        for point in self.snake_body_pos:
            matrix[point.x][point.y] = ObjectsCodes.SNAKE
        
        # allocate head
        matrix[self.snake_head_pos.x][self.snake_head_pos.y] = ObjectsCodes.SNAKE_HEAD
        
        # allocate apple
        matrix[self.apple_pos.x][self.apple_pos.y] = ObjectsCodes.APPLE
        
        return matrix

class SnakeSubconsole(SnakeBasic):
    '''
    Snake Basic but with an ability to display game in subconsole.
    '''
    def __init__(self, arena_size: tuple = (15, 15), color: str = "0a", name: str = "Snake Game"):
        global subconsole
        import subconsole

        # call parent constructor
        super().__init__(arena_size)

        # create console
        self.console = subconsole.console(color, name)
        # configure console
        self.console.call_commad(f'mode 30, 15')

        # display
        self.display()
    
    def display(self, Debug: bool = False):
        '''
        Displays sake game in subconsole.
        '''
        # clear console
        self.console.call_commad('cls')

        # print all of it
        for row in self._get_matrix():
            for cell in row:
                self.console.write(cell)
            self.console.write('\n')
        
        # display debug stuff
        if(Debug):
            self.console.write(f'\nHeadpos -> {self.snake_head_pos}')
            self.console.write(f'Direction -> {self.snake_direction}\n')
            self.console.write(f'Moves -> {self.moves}')
            self.console.write(f'Died -> {self.died}')

class SnakeWindowed(SnakeBasic):
    # static assets
    apple_sprite = None
    pixelfont = None
    
    def reset(self):
        super().reset()
        self.died_frame = False
    
    def __init__(self, arena_size: tuple = (15, 15), cell_size: int = 30):
        # add modules per class only
        global pygame, color_settings
        import color_settings, pygame, pygame.freetype
        
        # init pygame
        pygame.init()
        pygame.freetype.init()

        # init patrent constructor
        super().__init__(arena_size)
        self.cell_size = cell_size

        # handle death
        self.died_frame = False
        
        # usefull var
        self.width = cell_size * arena_size[0] + (arena_size[0] + 1)
        self.height =  cell_size * arena_size[1] + (arena_size[1] + 1)

        # --- SPRITES ---
        
        # load static assets ^-^
        if(SnakeWindowed.apple_sprite == None):
            SnakeWindowed.apple_sprite = pygame.image.load('./assets/Sprites/apple.png').convert()
            SnakeWindowed.apple_sprite.convert_alpha()
            SnakeWindowed.apple_sprite.set_colorkey((255, 255, 255))
            SnakeWindowed.apple_sprite = pygame.transform.scale(SnakeWindowed.apple_sprite, (self.cell_size, self.cell_size))
        if (SnakeWindowed.pixelfont == None):
            SnakeWindowed.pixelfont = pygame.freetype.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        
        # region pre-render grid 
        # drawing surface
        self.surface = pygame.Surface((cell_size * arena_size[0]+(arena_size[0]+1), cell_size*arena_size[1] + arena_size[1]+1))
        self._grid = pygame.Surface((cell_size * arena_size[0] + (arena_size[0]+1), cell_size * arena_size[1] + (arena_size[1] + 1)))
        
        # clear out the image
        self._grid.fill(color_settings.BCKG_GAME_COLOR)
        
        # draw vertical lines
        for i in range(1, arena_size[0]):
            pygame.draw.line(self._grid, color_settings.GRID_COLOR,
                            (i * self.cell_size + i, 0),
                            (i * self.cell_size + i, self._grid.get_height()),
                            width = 1)
            
        # draw horizontal lines
        for i in range(1, arena_size[1]):
            pygame.draw.line(self._grid, color_settings.GRID_COLOR,
                            (0, i * self.cell_size + i),
                            (self._grid.get_width(),i * self.cell_size + i),
                            width = 1)
            
        # frame
        pygame.draw.line(self._grid, color_settings.FRAME_COLOR, (0, 0), (self._grid.get_width(), 0), width = 1)
        pygame.draw.line(self._grid, color_settings.FRAME_COLOR, (0, 0), (0, self._grid.get_height()), width = 1)
        pygame.draw.line(self._grid, color_settings.FRAME_COLOR, (self._grid.get_width()-1, self._grid.get_height()), (self._grid.get_width() - 1, 0), 1)
        pygame.draw.line(self._grid, color_settings.FRAME_COLOR, (self._grid.get_width()-1, self._grid.get_height() - 1), (0, self._grid.get_height() - 1), 1)
        
        #endregion
    
    # draw game onto screen
    def draw(self, surface, offset = (0,0)):
        '''
        Draws element onto a surface(pygame)
        '''
        if self.died_frame == False:
            # draw grid on surface
            self.surface.blit(self._grid,(0, 0))
            
            # draw head
            pygame.draw.rect(
                    self.surface,
                    color_settings.SNAKE_COLOR,
                    (self.snake_body_pos[0].x * self.cell_size + self.snake_body_pos[0].x + 1,
                    self.snake_body_pos[0].y * self.cell_size + self.snake_body_pos[0].y + 1,
                    self.cell_size,
                    self.cell_size))
            
            # draw rest of body
            for index in range(len(self.snake_body_pos) - 1, 0, -1):
                deltapos = self.snake_body_pos[index - 1] - self.snake_body_pos[index]
                
                if deltapos.x == -1 and deltapos.y == 0:   
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index].x * self.cell_size + self.snake_body_pos[index].x,
                        self.snake_body_pos[index].y * self.cell_size + self.snake_body_pos[index].y + 1,
                        self.cell_size+1,
                        self.cell_size))
                elif deltapos.x == 1 and deltapos.y == 0:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index].x * self.cell_size + self.snake_body_pos[index].x + 1,
                        self.snake_body_pos[index].y * self.cell_size + self.snake_body_pos[index].y + 1,
                        self.cell_size + 1,
                        self.cell_size))
                elif deltapos.x == 0 and deltapos.y == -1:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index].x * self.cell_size + self.snake_body_pos[index].x + 1,
                        self.snake_body_pos[index].y * self.cell_size + self.snake_body_pos[index].y,
                        self.cell_size,
                        self.cell_size + 1))
                elif deltapos.x == 0 and deltapos.y == 1:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index].x * self.cell_size + self.snake_body_pos[index].x + 1,
                        self.snake_body_pos[index].y * self.cell_size + self.snake_body_pos[index].y + 1,
                        self.cell_size,
                        self.cell_size + 1))
                    
                self.surface.blit(SnakeWindowed.apple_sprite, (
                    self.apple_pos.x * self.cell_size + self.apple_pos.x+ 1,
                    self.apple_pos.y * self.cell_size + self.apple_pos.y+ 1,
                    self.cell_size,
                    self.cell_size))
                
            # draw an apple
            self.surface.blit(SnakeWindowed.apple_sprite, 
                (self.apple_pos.x * self.cell_size + self.apple_pos.x + 1,
                self.apple_pos.y * self.cell_size + self.apple_pos.y + 1,
                self.cell_size,
                self.cell_size))
            
            # draw cross if died
            if self.died:              
                pygame.draw.line(self.surface, color_settings.CROSS_COLOR, (0, 0), (self._grid.get_width(), self._grid.get_height()), width = 1)
                pygame.draw.line(self.surface, color_settings.CROSS_COLOR, (0, self._grid.get_height()), (self._grid.get_width(), 0), width = 1)
                
                
                text_rect = SnakeWindowed.pixelfont.get_rect('died', size = 20)
                text_rect.center = self.surface.get_rect().center 

                SnakeWindowed.pixelfont.render_to(self.surface, text_rect, 'died', color_settings.TEXT_COLOR, size = 20)
                
                self.died_frame = True
                
        surface.blit(self.surface, offset)

#
class Direction:
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    
    directions = [UP, DOWN, LEFT, RIGHT]

#
class ObjectsCodes:
    VOID = 0
    SNAKE = .5
    SNAKE_HEAD = 1
    APPLE = -1


