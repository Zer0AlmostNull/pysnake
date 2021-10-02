from enum import Enum
from random import choice

import color_settings
import pygame


class GameBase():
    def __init__(self, arena_size: tuple = (15, 15), cell_size: tuple = 30):
        # pass given properties into object
        self.cell_size = cell_size
        self.arena_size = arena_size
        
        self.arena_matrix = [[ObjectsCodes.VOID.value] * arena_size[1] for _ in range(arena_size[0])]
        self.free_spaces = [(y, x) for x in range(0, len(self.arena_matrix[0])) for y in range(0, len(self.arena_matrix))]
        
        # 
        self.map_area = arena_size[0] * arena_size[1]
        
        # set snake default direction
        self.snake_direction = Direction.UP
        
        # center snake's position
        self.snake_head_pos = [int(len(self.arena_matrix[0])/2), int(len(self.arena_matrix)/2)]
        self.free_spaces.remove((self.snake_head_pos[0], self.snake_head_pos[1]))
        
        
        # add head position to body position
        self.snake_body_pos = [self.snake_head_pos.copy()]
        
        
        # allocate area with snake's head
        self.arena_matrix[self.snake_head_pos[0]][self.snake_head_pos[1]] = ObjectsCodes.SNAKE_HEAD.value
        
        # allocate area with snake's blocks
        for pos in self.snake_body_pos[1:]:
            self.arena_matrix[pos[0]][pos[1]] = ObjectsCodes.SNAKE.value
            self.free_spaces.remove((pos[0], pos[1]))     
        
        
        # random pick random apple position    
        self.apple_pos = choice(self.free_spaces)
        self.free_spaces.remove(self.apple_pos)
        self.arena_matrix[self.apple_pos[0]][self.apple_pos[1]] = ObjectsCodes.APPLE.value
        
        # handle death
        self.died = False


    def tick(self, input_):
        """ Updates game"""
        # return if snake already died 
        if self.died:
            return ReturnCodes.DEATH_FRAME
        
        # input
        self.snake_direction = input_
            
        # move snake's head 
        self.snake_head_pos[0] += self.snake_direction.value[0]
        self.snake_head_pos[1] += self.snake_direction.value[1]
            
        # check if snake out of border
        if self.snake_head_pos[0] >= len(self.arena_matrix) or self.snake_head_pos[0] < 0 or \
        self.snake_head_pos[1] >= len(self.arena_matrix[0]) or self.snake_head_pos[1] < 0:         
            self.died = True
            return ReturnCodes.DIED
        
        # check if run into itself
        if self.arena_matrix[self.snake_head_pos[0]][self.snake_head_pos[1]] == ObjectsCodes.SNAKE.value:    
            self.died = True
            return ReturnCodes.DIED
        
        # check if its on apple
        if self.arena_matrix[self.snake_head_pos[0]][self.snake_head_pos[1]] == ObjectsCodes.APPLE.value:
            
            # update arena matrix
            self.arena_matrix[self.snake_body_pos[0][0]][self.snake_body_pos[0][1]] =  ObjectsCodes.SNAKE.value
            self.arena_matrix[self.snake_head_pos[0]][self.snake_head_pos[1]] = ObjectsCodes.SNAKE_HEAD.value
            
            # add a block to the snake 
            self.snake_body_pos.insert(0, [self.snake_head_pos[0], self.snake_head_pos[1]])
            
            # pick apple random position and del it from free spaces
            self.apple_pos = choice(self.free_spaces)
            self.free_spaces.remove(self.apple_pos)
            self.arena_matrix[self.apple_pos[0]][self.apple_pos[1]] = ObjectsCodes.APPLE.value
        
        else:
            # add tail position to free spaces 
            self.free_spaces.append((self.snake_body_pos[-1][0],self.snake_body_pos[-1][1]))
            
            # remove head pos from free spaces
            self.free_spaces.remove((self.snake_head_pos[0], self.snake_head_pos[1]))
            
            # update area list
            self.arena_matrix[self.snake_body_pos[0][0]][self.snake_body_pos[0][1]] =  ObjectsCodes.SNAKE.value
            self.arena_matrix[self.snake_body_pos[-1][0]][self.snake_body_pos[-1][1]] = ObjectsCodes.VOID.value
            self.arena_matrix[self.snake_head_pos[0]][self.snake_head_pos[1]] =  ObjectsCodes.SNAKE_HEAD.value
            
            # move the rest of the snake's body
            for i in range(len(self.snake_body_pos)-1, 0, -1):
                # move block
                self.snake_body_pos[i][0] = self.snake_body_pos[i-1][0]
                self.snake_body_pos[i][1] = self.snake_body_pos[i-1][1]
                
            # move head
            self.snake_body_pos[0] = [self.snake_head_pos[0], self.snake_head_pos[1]]
            
        return ReturnCodes.NOTHING
    
class GameGraphical(GameBase):
    def __init__(self, arena_size: tuple = (15, 15), cell_size: tuple = 30):
        # init patrent constructor
        super().__init__(arena_size, cell_size)

        # handle death
        self.died_frame = False

        # --- SPRITES ---
        
        # load apple sprite
        self.apple_sprite = pygame.image.load('./assets/Sprites/apple.png').convert()
        self.apple_sprite.convert_alpha()
        self.apple_sprite.set_colorkey((255, 255, 255))
        self.apple_sprite = pygame.transform.scale(self.apple_sprite, (self.cell_size, self.cell_size))
        
        #region pre-render grid 
        # drawing surface
        self.surface = pygame.Surface((cell_size * arena_size[0]+(arena_size[0]+1), cell_size*arena_size[1] + arena_size[1]+1))
        self.GRID = pygame.Surface((cell_size * arena_size[0] + (arena_size[0]+1), cell_size * arena_size[1] + (arena_size[1] + 1)))
        
        # clear out the image
        self.GRID.fill(color_settings.BCKG_GAME_COLOR)
        
        # draw vertical lines
        for i in range(1, arena_size[0]):
            pygame.draw.line(self.GRID, color_settings.GRID_COLOR,
                            (i * self.cell_size + i, 0),
                            (i * self.cell_size + i, self.GRID.get_height()),
                            width = 1)
            
        # draw horizontal lines
        for i in range(1, arena_size[1]):
            pygame.draw.line(self.GRID, color_settings.GRID_COLOR,
                            (0, i * self.cell_size + i),
                            (self.GRID.get_width(),i * self.cell_size + i),
                            width = 1)
            
        # frame
        pygame.draw.line(self.GRID, color_settings.FRAME_COLOR, (0, 0), (self.GRID.get_width(), 0), width = 1)
        pygame.draw.line(self.GRID, color_settings.FRAME_COLOR, (0, 0), (0, self.GRID.get_height()), width = 1)
        pygame.draw.line(self.GRID, color_settings.FRAME_COLOR, (self.GRID.get_width()-1, self.GRID.get_height()), (self.GRID.get_width() - 1, 0), 1)
        pygame.draw.line(self.GRID, color_settings.FRAME_COLOR, (self.GRID.get_width()-1, self.GRID.get_height() - 1), (0, self.GRID.get_height() - 1), 1)

    # draw game onto screen
    def draw(self, surface, offset = (0,0)):
        """ Draws element onto a surface """
        if self.died_frame == False:
            # draw grid on surface
            self.surface.blit(self.GRID,(0, 0))
            
            # draw head
            pygame.draw.rect(
                    self.surface,
                    color_settings.SNAKE_COLOR,
                    (self.snake_body_pos[0][0] * self.cell_size + self.snake_body_pos[0][0] + 1,
                    self.snake_body_pos[0][1] * self.cell_size + self.snake_body_pos[0][1] + 1,
                    self.cell_size,
                    self.cell_size))
            
            # draw rest of body
            for index in range(len(self.snake_body_pos) - 1, 0, -1):
                deltapos = (self.snake_body_pos[index-1][0]-self.snake_body_pos[index][0], self.snake_body_pos[index-1][1]-self.snake_body_pos[index][1])
                
                if deltapos[0] == -1 and deltapos[1] == 0:   
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index][0] * self.cell_size + self.snake_body_pos[index][0],
                        self.snake_body_pos[index][1] * self.cell_size + self.snake_body_pos[index][1] + 1,
                        self.cell_size+1,
                        self.cell_size)
                        )
                elif deltapos[0] == 1 and deltapos[1] == 0:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index][0] * self.cell_size + self.snake_body_pos[index][0] + 1,
                        self.snake_body_pos[index][1] * self.cell_size + self.snake_body_pos[index][1] + 1,
                        self.cell_size+1,
                        self.cell_size)
                        )
                elif deltapos[0] == 0 and deltapos[1] == -1:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index][0] * self.cell_size + self.snake_body_pos[index][0] + 1,
                        self.snake_body_pos[index][1] * self.cell_size + self.snake_body_pos[index][1],
                        self.cell_size,
                        self.cell_size+1)
                        )
                elif deltapos[0] == 0 and deltapos[1] == 1:
                    pygame.draw.rect(
                        self.surface,
                        color_settings.SNAKE_COLOR,
                        (self.snake_body_pos[index][0] * self.cell_size + self.snake_body_pos[index][0] + 1,
                        self.snake_body_pos[index][1] * self.cell_size + self.snake_body_pos[index][1] + 1,
                        self.cell_size,
                        self.cell_size+1)
                        )
                    
                self.surface.blit(self.apple_sprite, (
                    self.apple_pos[0] * self.cell_size+self.apple_pos[0]+ 1,
                    self.apple_pos[1] * self.cell_size+self.apple_pos[1]+ 1,
                    self.cell_size,
                    self.cell_size))
                
            # draw an apple
            self.surface.blit(self.apple_sprite, 
                (self.apple_pos[0] * self.cell_size + self.apple_pos[0] + 1,
                self.apple_pos[1] * self.cell_size + self.apple_pos[1] + 1,
                self.cell_size,
                self.cell_size))
            
            # draw cross if died
            if self.died:              
                pygame.draw.line(self.surface, color_settings.CROSS_COLOR, (0, 0), (self.GRID.get_width(), self.GRID.get_height()), width = 1)
                pygame.draw.line(self.surface, color_settings.CROSS_COLOR, (0, self.GRID.get_height()), (self.GRID.get_width(), 0), width = 1)
                
                pixelfont = pygame.freetype.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
                
                text_rect = pixelfont.get_rect('You died!', size = 30)
                text_rect.center = self.surface.get_rect().center 

                pixelfont.render_to(self.surface, text_rect, 'You died!', color_settings.TEXT_COLOR, size = 30)
                
                self.died_frame = True
                
        surface.blit(self.surface, offset)

# enum direction
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
        
# enum objects codes
class ObjectsCodes(Enum):
    VOID = 0
    SNAKE = 1
    SNAKE_HEAD = 2
    APPLE = 5

class ReturnCodes(Enum):
    NOTHING = 0
    DIED = 1
    DEATH_FRAME = 2
