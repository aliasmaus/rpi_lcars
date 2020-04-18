import sys
import pygame
import config

from ui import colours
from ui.utils.sound import Sound
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import LcarsText
from ui.widgets.screen import LcarsScreen
from ui.widgets.lcars_widgets import LcarsButton, UltimateButton

class ScreenAuthorize(LcarsScreen):

    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_2_modern.png"),
                        layer=0)

        all_sprites.add(LcarsGifImage("assets/gadgets/stlogorotating.gif", (103, 369), 50), 
                        layer=0)        

        all_sprites.add(LcarsText(colours.BLUEMID, (270, -1), "AUTHORIZATION REQUIRED", 2),
                        layer=1)

        all_sprites.add(LcarsText(colours.BLUEMID, (330, -1), "ONLY AUTHORIZED PERSONNEL MAY ACCESS THIS TERMINAL", 1.5),
                        layer=1)

        all_sprites.add(LcarsText(colours.BLUEMID, (360, -1), "TOUCH TERMINAL TO PROCEED", 1.5),
                        layer=1)
        
        #all_sprites.add(LcarsText(colours.BLUE, (390, -1), "FAILED ATTEMPTS WILL BE REPORTED", 1.5),layer=1)
        button_row_1 = 230
        button_row_2 = 270
        button_row_3 = 310
        button_row_4 = 350
        button_col_1 = 210
        button_col_2 = 340
        button_col_3 = 470
        button_image = pygame.image.load("assets/buttonpad.png")
        button_image_down = pygame.image.load("assets/buttonpaddown.png")
        all_sprites.add(UltimateButton((button_row_1, button_col_1), text="1", handler=self.num_1, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_1, button_col_2), text="2", handler=self.num_2, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_1, button_col_3), text="3", handler=self.num_3, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_2, button_col_1), text="4", handler=self.num_4, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_2, button_col_2), text="5", handler=self.num_5, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_2, button_col_3), text="6", handler=self.num_6, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_3, button_col_1), text="7", handler=self.num_7, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_3, button_col_2), text="8", handler=self.num_8, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_3, button_col_3), text="9", handler=self.num_3, image_set=[button_image, button_image, button_image_down]), layer=2)
        all_sprites.add(UltimateButton((button_row_4, button_col_2), text="0", handler=self.num_7, image_set=[button_image, button_image, button_image_down]), layer=2)


        if config.DEV_MODE:
            all_sprites.add(LcarsButton(colours.GREY_BLUE, (0, 770), "X", self.exitHandler, (30, 30)), layer=2)
        
        self.layer1 = all_sprites.get_sprites_from_layer(1)
        self.layer2 = all_sprites.get_sprites_from_layer(2)

        # sounds
        Sound("assets/audio/panel/215.wav").play()
        self.sound_granted = Sound("assets/audio/accessing.wav")
        self.sound_beep1 = Sound("assets/audio/panel/201.wav")
        self.sound_denied = Sound("assets/audio/access_denied.wav")
        self.sound_deny1 = Sound("assets/audio/deny_1.wav")
        self.sound_deny2 = Sound("assets/audio/deny_2.wav")

        ############
        # SET PIN CODE WITH THIS VARIABLE
        ############
        self.pin = 1337
        ############
        self.reset()

    def reset(self):
        # Variables for PIN code verification
        self.correct = 0
        self.pin_i = 0
        self.granted = False
        for sprite in self.layer1: sprite.visible = True
        for sprite in self.layer2: sprite.visible = False

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Play sound
            self.sound_beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            if (not self.layer2[0].visible):
                for sprite in self.layer1: sprite.visible = False
                for sprite in self.layer2: sprite.visible = True
                Sound("assets/audio/enter_authorization_code.wav").play()
            elif (self.pin_i == len(str(self.pin))):
                # Ran out of button presses
                if (self.correct == len(str(self.pin))):
                    self.sound_granted.play()
                    from screens.main import ScreenMain
                    self.loadScreen(ScreenMain())
                else:
                    self.sound_deny2.play()
                    self.sound_denied.play()
                    self.reset()

        return False

    def num_1(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '1':
            self.correct += 1

        self.pin_i += 1

    def num_2(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '2':
            self.correct += 1

        self.pin_i += 1

    def num_3(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '3':
            self.correct += 1

        self.pin_i += 1

    def num_4(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '4':
            self.correct += 1

        self.pin_i += 1

    def num_5(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '5':
            self.correct += 1

        self.pin_i += 1

    def num_6(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '6':
            self.correct += 1

        self.pin_i += 1

    def num_7(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '7':
            self.correct += 1

        self.pin_i += 1

    def num_8(self, item, event, clock):
        if str(self.pin)[self.pin_i] == '8':
            self.correct += 1

        self.pin_i += 1

    def exitHandler(self, item, event, clock):
        sys.exit()
