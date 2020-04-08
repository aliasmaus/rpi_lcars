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
                    image.get_rect().height - textImage.get_rect().height - 5))
    
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
            image = pygame.image.load("assets/elbow_bottom_down.png").convert_alpha()
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
                    image.get_rect().height - textImage.get_rect().height - 5))
    
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
            self.applyColour(self.colour)
           
        return GeneralWidget.handleEvent(self, event, clock)


class UltimateButton(LcarsWidget):
    """
    
        THE ULTIMATE BUTTON DOES EVERYTHING YOU NEED
        make it simple or fancy, your choice :D
        
        Button will be generated depending on arguments supplied
        -- no colours/images = default colours square button
        -- colours only = custom colours square button
        -- images only = custom image button
        -- 1 image no colours = default colours shape button
        -- 1 image + colors = custom colours shape button
        
        colour_ set should be formatted [colour, colour_highlighted, colour_pressed]
        image_set should be formatted [image, image_highlighted, image_pressed] OR [image] (array of length 1)
        
        tested working:
        -- no colours/images
        -- colours only
        -- 1 image no colours
        -- 1 image + colours
        -- buttons with text
        
        theoretically working but untested:
        -- 3 images (image set)
        
    """
    
    #DEFAULTS
    colour=colours.WHITE
    colour_highlighted=colours.GREY_BLUE
    colour_pressed=colours.BLUE
    image_normal=None
    image_highlighted=None
    image_pressed=None
    size=(80, 40)
    text=""
    text_colour=colours.BLACK
    imageonly=False    
    
    def __init__(self, pos, size=None, text=None, colour_set=None, image_set=None, text_colour=None, font=None, handler=None):        
        
        #If colour or image sets are supplied, update defaults
        if not colour_set == None:
            self.colour=colour_set[0]
            self.colour_highlighted=colour_set[1]
            self.colour_pressed=colour_set[2]
            if not size == None:
                self.size = size
        if not image_set == None:
            image=image_set[0].convert_alpha()
            if len(image_set) > 1:
                self.image_highlighted=image_set[1].convert_alpha()
                self.image_pressed=image_set[2].convert_alpha()
            self.size = (image.get_rect().width, image.get_rect().height)
        if not text_colour == None:
            self.text_colour = text_colour
        
        #Create surface for non-image button
        if image_set == None:
            image = pygame.Surface(self.size)
            image.fill(self.colour)
            
        self.image = image
        #Create text image
        if not text==None:
            if font == None:
                self.font = Font("assets/MicroTech.ttf", 18)
            else:
                self.font = font
            textImage = self.font.render(text, False, self.text_colour)
            #textrect = textImage.get_rect()
            image = image.blit(textImage, 
                        (image.get_rect().width - textImage.get_rect().width - 10,
                            image.get_rect().height - textImage.get_rect().height - 5))
            #if not self.image_pressed==None:
             #   self.image_pressed = self.image_pressed.blit(textImage, 
              #              (image.get_rect().width - textImage.get_rect().width - 10,
               #                 image.get_rect().height - textImage.get_rect().height - 5))
        #
        #Make widget 
        LcarsWidget.__init__(self, self.colour, pos, self.size, handler)
        if image_set == None:
            self.applyColour(self.colour)
        elif len(image_set) == 1 and not colour_set==None:
            self.applyColour(self.colour)
        else:
            self.imageonly=True
        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")   
    
    def handleEvent(self, event, clock):
        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            if self.image_pressed == None and self.imageonly==False:
                self.applyColour(self.colour_pressed)
                self.highlighted = True
                self.beep.play()
            else:
                self.image_normal=self.image
                if not self.image_pressed==None:
                    self.image = self.image_pressed
        
        #need to add mouseover highlight functionality here
        
        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            if self.image_pressed == None and self.imageonly==False:
                self.applyColour(self.colour)
            else:
                self.image = self.image_normal
           
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
            
        LcarsWidget.__init__(self, colour, pos, None, handler)

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
        
class ClusterButton(ModernElbowTop):
    
    def __init__(self, colour, pos, text, group_number, handler=None, rectSize=None, icon=None):
        self.group_number=group_number
        ModernElbowTop.__init__(self, colour, pos, text, handler)

        
        
