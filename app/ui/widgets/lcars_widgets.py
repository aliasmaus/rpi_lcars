import pygame
from pygame.font import Font
from pygame.locals import *

from ui.utils.sound import Sound
from ui.widgets.sprite import LcarsWidget, PowerWidget, ResetWidget
from ui import colours

class LcarsElbow(LcarsWidget):
    """The LCARS corner elbow - not currently used"""
    
    STYLE_BOTTOM_LEFT = 0
    STYLE_TOP_LEFT = 1
    STYLE_BOTTOM_RIGHT = 2
    STYLE_TOP_RIGHT = 3
    
    def __init__(self, colour, style, pos, handler=None):
        image = pygame.image.load("assets/elbow.png").convert_alpha()
        # alpha=255
        # image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        if (style == LcarsElbow.STYLE_BOTTOM_LEFT):
            image = pygame.transform.flip(image, False, True)
        elif (style == LcarsElbow.STYLE_BOTTOM_RIGHT):
            image = pygame.transform.rotate(image, 180)
        elif (style == LcarsElbow.STYLE_TOP_RIGHT):
            image = pygame.transform.flip(image, True, False)
        
        self.image = image
        size = (image.get_rect().width, image.get_rect().height)
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.applyColour(colour)

class LcarsTab(LcarsWidget):
    """Tab widget (like radio button) - not currently used nor implemented"""

    STYLE_LEFT = 1
    STYLE_RIGHT = 2
    
    def __init__(self, colour, style, pos, handler=None):
        image = pygame.image.load("assets/tab.png").convert()
        if (style == LcarsTab.STYLE_RIGHT):
            image = pygame.transform.flip(image, False, True)
        
        size = (image.get_rect().width, image.get_rect().height)
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.image = image
        self.applyColour(colour)

class LcarsButton(LcarsWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""

    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/button.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            image.fill(colour)

        self.colour = colour
        self.image = image
        font = Font("assets/swiss911.ttf", 19)
        textImage = font.render(text, False, colours.BLACK)
        image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 10,
                    image.get_rect().height - textImage.get_rect().height - 5))
        if not icon==None:
            image.blit(icon, (10,10))
    
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.applyColour(colour)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.applyColour(colours.WHITE)
            self.highlighted = True
            self.beep.play()

        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.applyColour(self.colour)
           
        return LcarsWidget.handleEvent(self, event, clock)

class PowerButton(PowerWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""
    
    
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/power_small_cyan.png")
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            image.fill(colour)

        self.colour = colour
        self.image = image.convert_alpha()
        #font = Font("assets/swiss911.ttf", 8)
        #textImage = font.render(text, False, colours.BLACK)
        #image.blit(textImage, 
        #        (image.get_rect().width - textImage.get_rect().width - 10,
        #            image.get_rect().height - textImage.get_rect().height - 5))
        #if not icon==None:
        #    image.blit(icon, (10,10))
    
        PowerWidget.__init__(self, colour, pos, size, handler)
        #self.applyColour(colour)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        image2 = pygame.image.load("assets/power_small.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            #self.applyColour(colours.WHITE)
            self.highlighted = True
            self.beep.play()
            self.image = image2.convert_alpha()
            #size = (image.get_rect().width, image.get_rect().height)


        #self.colour = colour
        
        image = pygame.image.load("assets/power_small_cyan.png")
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = image.convert_alpha()
           
        return PowerWidget.handleEvent(self, event, clock)
        
class ResetButton(ResetWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""

    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/reset_small_cyan.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            image.fill(colour)

        self.colour = colour
        self.image = image
    
        PowerWidget.__init__(self, colour, pos, size, handler)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        image2 = pygame.image.load("assets/reset_small.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.highlighted = True
            self.beep.play()
            self.image = image2.convert_alpha()

        
        image = pygame.image.load("assets/reset_small_cyan.png")
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = image.convert_alpha()
           
        return PowerWidget.handleEvent(self, event, clock)
                
class LcarsText(LcarsWidget):
    """Text that can be placed anywhere"""

    def __init__(self, colour, pos, message, size=1.0, background=None, handler=None):
        self.colour = colour
        self.background = background
        self.font = Font("assets/swiss911.ttf", int(19.0 * size))
        
        self.renderText(message)
        # center the text if needed 
        if (pos[1] < 0):
            pos = (pos[0], 400 - self.image.get_rect().width / 2)
            
        LcarsWidget.__init__(self, colour, pos, None, handler)

    def renderText(self, message):        
        if (self.background == None):
            self.image = self.font.render(message, True, self.colour)
        else:
            self.image = self.font.render(message, True, self.colour, self.background)
        
    def setText(self, newText):
        self.renderText(newText)

class LcarsBlockLarge(LcarsButton):
    """Left navigation block - large version"""

    def __init__(self, colour, pos, text, handler=None):
        size = (98, 147)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockMedium(LcarsButton):
   """Left navigation block - medium version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (98, 62)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockSmall(LcarsButton):
   """Left navigation block - small version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (98, 34)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

class RelayPowerButton(PowerButton):

    def __init__(self, colour, pos, text, relayController, handler=None, rectSize=None, icon=None):
        self.relay=relayController
        PowerButton.__init__(self, colour, pos, text, handler, icon=icon)

class RelayResetButton(ResetButton):

    def __init__(self, colour, pos, text, relayController, handler=None, rectSize=None, icon=None):
        self.relay=relayController
        ResetButton.__init__(self, colour, pos, text, handler, icon=icon)
        
class ClusterButton(LcarsButton):
    
    def __init__(self, colour, pos, text, group_number, handler=None, rectSize=None, icon=None):
        self.group_number=group_number
        LcarsButton.__init__(self, colour, pos, text, handler)
