import pygame
import pygame.freetype
from enum import Enum

def create_surface_with_text(text, font_size, text_rgb, bg_rgb, font_name = 'Verdana', bold = True):
    font = None
    if '.' in font_name:
        font = pygame.freetype.Font(font_name, font_size)
    else:
        font = pygame.freetype.SysFont(font_name, font_size, bold = bold)
    

    surface, _ = font.render(text = text, fgcolor = text_rgb, bgcolor = (bg_rgb if bg_rgb != False else (0,0,0,0)))
    return surface.convert_alpha()

class UIElement(pygame.sprite.Sprite):
    
    class Anchor(Enum):
        CENTER = 0
        TL = 1
    
    def __init__(self, position, text, font_size, bg_rgb, text_rgb, text_rgb_highlight, clickedAction = None, font = 'Verdana', hoover_multiplier = 1.2, bold = True, anchor = Anchor.CENTER):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            text_rgb_highlight (text colour) - tuple (r, g, b)
        """
        # indicates if the mouse is over the element
        self.mouse_over = False  
        
        # contains method
        self.clickedAction = clickedAction 

        # create the default image
        default_image = create_surface_with_text(
            text = text, 
            font_size = font_size, 
            text_rgb = text_rgb, 
            bg_rgb = bg_rgb, 
            font_name = font,
            bold = bold
        )

        # create hovered image
        highlighted_image = create_surface_with_text(
            text = text,
            font_size = font_size * hoover_multiplier,
            text_rgb = text_rgb_highlight,
            bg_rgb = bg_rgb,
            font_name = font,
            bold = bold
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = []
        
        # handle handle anchor
        if anchor == self.Anchor.CENTER:
            self.rects = [
                default_image.get_rect(center = position),
                highlighted_image.get_rect(center = position),
            ]
        elif anchor == self.Anchor.TL:
            self.rects = [
                default_image.get_rect(topleft = position),
                highlighted_image.get_rect(topleft = position),
            ]

        # calls the init method of the parent sprite class
        super().__init__()
        
    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.clickedAction
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)