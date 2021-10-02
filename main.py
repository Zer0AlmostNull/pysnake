from os import environ

# hide pygame version info
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from game import Direction, GameGraphical, ReturnCodes
from ui import UIElement
import pygame
import game_settings, color_settings
from game_state import GameState

def main():
    
    # init pygame main module and font module
    pygame.init()
    pygame.font.init()
    
    # create display object - window with given size
    screen = pygame.display.set_mode((game_settings.WND_WIDTH, game_settings.WND_HEIGHT))
    
    # set that window's title
    pygame.display.set_caption(game_settings.TITLE_TEXT)
    
    # set default game state to main menu
    game_state = GameState.MAINMENU
    
    # main loop of game
    while True:
        
        # start diffrent function for each game state and get next game state
        if game_state == GameState.MAINMENU:
            game_state = main_menu(screen)
            
        elif game_state == GameState.GAME:
            game_state = new_game(screen)
            
        elif game_state == GameState.QUIT:
            # quit pygame module
            pygame.quit()
            return

def main_menu(screen):
    # get pixel font from file
    pixelFont70 = pygame.freetype.Font("assets/fonts/PressStart2P-Regular.ttf", 70)
    
    # create a UI Elements acting like a buttons
    # I've got here a little of hardcoded shit. Please do not cry.
    btnStartGame = UIElement(
        position = (game_settings.WND_WIDTH//2, 350),
        text = "Start Game",
        font_size = 45,
        bg_rgb = color_settings.BCKG_COLOR,
        text_rgb = (200, 200, 200),
        text_rgb_highlight = (255, 255, 255),
        clickedAction = GameState.GAME,
        font = "assets/fonts/PressStart2P-Regular.ttf",
        bold = True,
        anchor = UIElement.Anchor.CENTER
    )
    
    btnQuit = UIElement(
        position = (game_settings.WND_WIDTH//2, 400),
        text = "QUIT",
        font_size = 25,
        bg_rgb = color_settings.BCKG_COLOR,
        text_rgb = (200, 200, 200),
        text_rgb_highlight = (255, 255, 255),
        clickedAction = GameState.QUIT,
        font = "assets/fonts/PressStart2P-Regular.ttf",
        bold = True,
        anchor = UIElement.Anchor.CENTER
    )
    
    # create a list of buttons
    buttons = [btnStartGame, btnQuit]
    
    # main menu clock
    clock = pygame.time.Clock()

    
    # init variables used in animated title color
    r, g, b, c = 0, 0, 0, 0
    
    
    # main window loop
    while True:
        # clear the screen
        screen.fill(color_settings.BCKG_COLOR)
        
        # controll fps via clock
        clock.tick(game_settings.FPS)
        
        # 
        mouse_up = False
        
        # iterate through pygame's events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT
        
        # check every button
        for button in buttons:
            # update button
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            # check response from button
            if ui_action is not None:
                return ui_action
            
            # draw button
            button.draw(screen)
        
        # render the title
        pixelFont70.render_to(
            surf = screen,
            text = game_settings.TITLE_TEXT, 
            fgcolor = (r, g, b), 
            bgcolor = color_settings.BCKG_COLOR,
            dest = (70, 100)
            )

        # title color changing animation
        if c == 0:
            r += 17
            c = 1
        elif c == 1:
            g += 17
            c = 2
        elif c == 2:
            b += 17
            c = 2
            
        if r >= 255:
            r, g, b, c = 0, 0, 0, 0
        elif g >= 255:
            b, g, c = 0, 0, 0
        elif b >= 255:
            c, b = 1, 0
        
        
        # update the screen
        pygame.display.update()
        
def new_game(screen):
    # get pixel font from file
    pixelFont = pygame.freetype.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
    
    # init game object
    game = GameGraphical(
        arena_size = game_settings.GAME_SIZE,
        cell_size = game_settings.CELL_SIZE)
    
    # game clock
    clock = pygame.time.Clock()
    timer = game_settings.TICK_INTERVAL
    
    # set few game's settings
    direction = Direction.UP
    score_offset = (int((game_settings.WND_WIDTH - game.surface.get_width()) * 0.5), 5)
    game_offset = (score_offset[0], score_offset[1] + 26)

    # main game loop
    while 1:
        # handling events
        for event in pygame.event.get():
            # quiting from an app
            if event.type == pygame.QUIT:
                return GameState.MAINMENU
            # handling keys input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    direction = Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    direction = Direction.DOWN
                elif event.key == pygame.K_UP:
                    direction = Direction.UP

                    
        # handle interval betwen ticks
        if timer > game_settings.TICK_INTERVAL:
            timer -= game_settings.TICK_INTERVAL
            
            # handle input
            #for event in pygame.event.get():

            
            # game update game
            return_code = game.tick(direction)
            if return_code == ReturnCodes.DIED:  
                # exit after death
                died = True
            elif return_code == ReturnCodes.DEATH_FRAME:
                pass

        # draw game
        game.draw(screen, game_offset)


        # draw points
        pixelFont.render_to(
            screen,
            score_offset,
            f"Points: {len(game.snake_body_pos)-1}",
            fgcolor = color_settings.TEXT_COLOR,
            bgcolor = color_settings.BCKG_COLOR,
            size = 25)
        
        
        # update the screen
        pygame.display.update()
        
        # clearing out the window
        screen.fill(color_settings.BCKG_COLOR)
        
        # control fps and get the interval
        timer += clock.tick(game_settings.FPS)

# run main func
if(__name__=="__main__"):
    main()