import pygame
from pygame.font import Font, SysFont
from pygame.locals import *

from ui.utils.sound import Sound
from ui.widgets.sprite import LcarsWidget, PowerWidget, ResetWidget, GeneralWidget
from ui import colours

class ModernButton(LcarsWidget):
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/button_modern.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize)
            image.fill(colour)
            #image=image.convert_alpha()

        self.colour = colours.TRANSPARENT
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 20)
        textImage = self.font.render(text, False, colours.BLUEDARK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 4,
                    image.get_rect().height - textImage.get_rect().height - 5))
        
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.applyColour(colour)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        image2 = pygame.image.load("assets/button_modern_down.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.highlighted = True
            self.beep.play()
            self.image = image2.convert_alpha()

        image = pygame.image.load("assets/button_modern.png")
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = image.convert_alpha()
           
        return LcarsWidget.handleEvent(self, event, clock)

class ModernElbowTop(GeneralWidget):
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/elbow_top.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            #image.fill(colours.TRANSPARENT)
            #image=image.convert_alpha()

        self.colour = colours.TRANSPARENT
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 20)
        textImage = self.font.render(text, False, colours.BLUEDARK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 170,
                    image.get_rect().height - textImage.get_rect().height - 10))
    
        GeneralWidget.__init__(self, colour, pos, size, handler)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")



    def handleEvent(self, event, clock):
        image2 = pygame.image.load("assets/elbow_top_up.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.image = image2.convert_alpha()
            self.highlighted = True
            self.beep.play()
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.applyColour(self.colour)
           
        return GeneralWidget.handleEvent(self, event, clock)
        
class ModernElbowBottom(GeneralWidget):
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/elbow_bottom.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            #image.fill(colours.TRANSPARENT)
            #image=image.convert_alpha()

        self.colour = colours.TRANSPARENT
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 20)
        textImage = self.font.render(text, False, colours.BLUEDARK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 185,
                    image.get_rect().height - textImage.get_rect().height - 30))
        #self.image1 = image
        GeneralWidget.__init__(self, colour, pos, size, handler)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")



    def handleEvent(self, event, clock):
        image2 = pygame.image.load("assets/elbow_bottom_down.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.image = image2.convert_alpha()
            self.highlighted = True
            self.beep.play()
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            #self.image = self.image1
            self.applyColour(self.colour)
           
        return GeneralWidget.handleEvent(self, event, clock)


class UltimateButton(LcarsWidget):
    """
    
        THE ULTIMATE BUTTON DOES EVERYTHING YOU NEED
        
        ARGUMENTS:
        *Required
            -position | (x coord, y coord)
        *Optional
            -size       | (width, height)                               default is (80, 40) or size of image_set[0]
            -text       | "string"                                      default is None
            -colour_set | [colour, colour_highlighted, colour_pressed]  default is [white, grey/blue, blue]
            -image_set  | [image, image_highlighted, image_pressed]     default is [None, None, None]
            -text_colour| (r, g, b) or from colours file                default is black
            -font       | pygame.Font                                   default is MicroTech
            -handler    | event handler function                        default is None
        
       BUGS:
        -- 3 images (image set) - text disappears when clicking
        
    """
    
    #DEFAULTS
    imageonly=False    
    #init
    def __init__(self, pos, text=None, colour_set=[colours.WHITE, colours.GREY_BLUE, colours.BLUE], image_set=[None,None,None], text_colour=colours.BLACK, font=None, size=(80,40), handler=None):        
        
        #Set button attributes
        #all buttons
        self.colour=colour_set[0]
        self.colour_highlighted=colour_set[1]
        self.colour_pressed=colour_set[2]
        self.size = size
        self.text_colour = text_colour
        #image buttons only
        if not image_set[0] == None:
            self.image_normal=image_set[0].convert_alpha()
            image=self.image_normal
            self.image=image
            self.size = (image.get_rect().width, image.get_rect().height)
        if not image_set[1] == None:
            self.image_highlighted=image_set[1].convert_alpha()
        if not image_set[2] == None:
            self.image_pressed=image_set[2].convert_alpha()
            self.imageonly=True
        #Create surface for non-image button
        if not self.imageonly:
            if image_set[0]==None:
                image = pygame.Surface(self.size)
                image.fill(self.colour)
                self.image=image
            #apply colour to white button
            else:
                self.image=image
                self.applyColour(self.colour)
            
        

        #Create text image if text included
        if not text==None:
            if font == None:
                self.font=Font("assets/MicroTech.ttf", 18)
            else:
                self.font = font
            textImage = self.font.render(text, False, self.text_colour)
            textrect = textImage.get_rect()
            image = image.blit(textImage, 
                        (image.get_rect().width - textImage.get_rect().width - 52,
                            image.get_rect().height - textImage.get_rect().height - 10))
        
        #Make widget 
        LcarsWidget.__init__(self, self.colour, pos, self.size, handler)
        if image_set[2] == None:
            self.applyColour(self.colour)
        else:
            self.imageonly=True
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")   
    #handle events
    def handleEvent(self, event, clock):
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            if self.imageonly:
                self.image = self.image_pressed
            else:
                self.applyColour(self.colour_pressed)
            self.highlighted = True
            self.beep.play()
        
        #need to add mouseover highlight functionality here
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            if self.imageonly:
                self.image = self.image_normal                
            else:
                self.applyColour(self.colour)
           
        return LcarsWidget.handleEvent(self, event, clock)



class SideButton(GeneralWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/button_modern.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            image.fill(colours.TRANSPARENT)
            
        #self.colour = colour
        #self.image = image
        #self.font = Font("assets/swiss911.ttf", 18)
        #textImage = self.font.render(text, False, colours.BLACK)
        #image = image.blit(textImage, 
        #        (image.get_rect().width - textImage.get_rect().width - 10,
        #            image.get_rect().height - textImage.get_rect().height - 5))

        self.colour = colours.TRANSPARENT
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 20)
        textImage = self.font.render(text, False, colours.BLUEDARK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 4,
                    image.get_rect().height - textImage.get_rect().height - 5))
    
        GeneralWidget.__init__(self, colour, pos, size, handler)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        #image2 = pygame.image.load("assets/reset_small.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.applyColour(colours.WHITE)
            self.highlighted = True
            self.beep.play()
            
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.applyColour(self.colour)
           
        return GeneralWidget.handleEvent(self, event, clock)
        
        
class LogoutButton(GeneralWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""
    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/button_modern.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize).convert_alpha()
            image.fill(colour)

    
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 19)
        textImage = self.font.render(text, False, colours.BLUEDARK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 5,
                    image.get_rect().height - textImage.get_rect().height))
    
        GeneralWidget.__init__(self, colour, pos, size, handler)
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def handleEvent(self, event, clock):
        #image2 = pygame.image.load("assets/reset_small.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.applyColour(colours.WHITE)
            self.highlighted = True
            self.beep.play()
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.applyColour(colours.TRANSPARENT)
           
        return GeneralWidget.handleEvent(self, event, clock)


class LcarsElbow(LcarsWidget):
    """The LCARS corner elbow - not currently used"""
    
    STYLE_BOTTOM_LEFT = 0
    STYLE_TOP_LEFT = 1
    STYLE_BOTTOM_RIGHT = 2
    STYLE_TOP_RIGHT = 3
    
    def __init__(self, colour, style, pos, text, group_number, handler):
        image = pygame.image.load("assets/elbow_top.png").convert_alpha()
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
        self.applyColour(colours.WHITE)
        
    def handleEvent(self, event, clock):
        #image2 = pygame.image.load("assets/reset_small.png")
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.applyColour(colours.WHITE)
            self.highlighted = True
            #self.beep.play()
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.applyColour(colours.TRANSPARENT)
           
        return GeneralWidget.handleEvent(self, event, clock)

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
            image = pygame.Surface(rectSize)
            image.fill(colour)
            #image=image.convert_alpha()

        self.colour = colour
        self.image = image
        self.font = Font("assets/YukonTech.ttf", 18)
        textImage = self.font.render(text, False, colours.BLACK)
        image = image.blit(textImage, 
                (image.get_rect().width - textImage.get_rect().width - 10,
                    image.get_rect().height - textImage.get_rect().height - 5))
        
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
            image = pygame.image.load("assets/power_small_cyantest.png")
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
        
        image = pygame.image.load("assets/power_small_cyantest.png")
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = image.convert_alpha()
           
        return PowerWidget.handleEvent(self, event, clock)
        
class ResetButton(ResetWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""

    def __init__(self, colour, pos, text, handler=None, rectSize=None, icon=None):
        if rectSize == None:
            image = pygame.image.load("assets/reset_small_cyantest.png").convert_alpha()
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

        image = pygame.image.load("assets/reset_small_cyantest.png")
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = image.convert_alpha()
           
        return PowerWidget.handleEvent(self, event, clock)
                
class LcarsText(LcarsWidget):
    """Text that can be placed anywhere"""

    def __init__(self, colour, pos, message, size=1.0, background=None, handler=None):
        self.colour = colour
        self.background = background
        self.font = Font("assets/MicroTech.ttf", int(15 * size))
        
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

class DescText(LcarsWidget):
    """Text that can be placed anywhere"""

    def __init__(self, colour, pos, message, size=1.6, background=None, handler=None):
        self.colour = colour
        self.background = background
        self.font = Font("assets/Doboto.ttf", int(15 * size))
        
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

class YukonText(LcarsWidget):
    """Text that can be placed anywhere"""

    def __init__(self, colour, pos, message, size=1.0, background=None, handler=None):
        self.colour = colour
        self.background = background
        self.font = Font("assets/YukonTech.ttf", int(20 * size))
        
        self.renderText(message)
        # center the text if needed 
        if (pos[1] < 0):
            pos = (pos[0], 400 - self.image.get_rect().width / 2)
            
        GeneralWidget.__init__(self, colour, pos, None, handler)

    def renderText(self, message):        
        if (self.background == None):
            self.image = self.font.render(message, True, self.colour)
        else:
            self.image = self.font.render(message, True, self.colour, self.background)
        
    def setText(self, newText):
        self.renderText(newText)

class LcarsBlockLarge(SideButton):
    """Left navigation block - large version"""

    def __init__(self, colour, pos, text, handler=None):
        size = (98, 147)
        SideButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockMedium(SideButton):
   """Left navigation block - medium version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (98, 62)
        SideButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockSmall(SideButton):
   """Left navigation block - small version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (98, 34)
        SideButton.__init__(self, colour, pos, text, handler, size)
        
class SideBlockSmall(LogoutButton):
   """Left navigation block - small version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (92, 15)
        LogoutButton.__init__(self, colour, pos, text, handler, size)

class RelayPowerButton(PowerButton):

    def __init__(self, colour, pos, text, relayController, handler=None, rectSize=None, icon=None):
        self.relay=relayController
        PowerButton.__init__(self, colour, pos, text, handler, icon=icon)

class RelayResetButton(ResetButton):

    def __init__(self, colour, pos, text, relayController, handler=None, rectSize=None, icon=None):
        self.relay=relayController
        ResetButton.__init__(self, colour, pos, text, handler, icon=icon)
        
class ClusterButton(UltimateButton):
    colour_set = [colours.WHITE, colours.GREY_BLUE, colours.BLUE]
    def __init__(self, pos, text, group_number, handler=None, colour_set=colour_set, image_set=[None, None, None]):
        self.group_number=group_number
        UltimateButton.__init__(self, pos, text, colour_set=colour_set, image_set=image_set, handler=handler)

        
        
