from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen

from controllers.relaycontroller import relaycontroller as RC

from datasources.network import get_ip_address_string
import pandas as pd
import gpiozero
from RPi import GPIO

class ScreenMain(LcarsScreen):
    relay_controllers=[]
    label_xpos=160
    pwr_button_xpos=250
    reset_button_xpos=350
    cluster_button_xpos=140
    cluster_button_ypos=120
    cluster_button_xinterval=140
    content_ypos=200
    content_yinterval=60
    cluster_node_labels=[]
    cluster_node_pwr_buttons=[]
    cluster_node_reset_buttons=[]
    cluster_buttons=[]
    title_text=None
    #power_icon=pygame.image.load("assets/power_small.png")
    #reset_icon=pygame.image.load("assets/reset_small.png").convert_alpha()

    def setup(self, all_sprites):
        #relay setup
        # get configuration from file
        pins_df=pd.read_csv("data/buttons.csv")
        self.all_sprites=all_sprites
        
        #loop through each cluster
        for i in range(pins_df['group'].max()):
            #create a button for top menu
            button = ClusterButton(colours.WHITE, (self.cluster_button_ypos, self.cluster_button_xpos+(self.cluster_button_xinterval*i)), "BANK "+ str(i+1), i+1, self.clusterButtonHandler)
            all_sprites.add(button, layer=4)
            self.cluster_buttons.append(button)
            #create arrays for labels, power/reset buttons
            self.cluster_node_labels.append([])
            self.cluster_node_pwr_buttons.append([])
            self.cluster_node_reset_buttons.append([])
            
        
        #loop through each machine
        for i in range(len(pins_df)):
            button=None
            label=None
            controller=RC(int(pins_df['gpio_pin'][i]))
            self.relay_controllers.append(controller)
        #create relevant button and add it to all_sprites and button array
        #buttons not in group 1 hidden by default
        #creates labels with power buttons
            if pins_df['type'][i]=='power':
                name=pins_df['name'][i]
                button=RelayPowerButton(colours.PURPLE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.pwr_button_xpos), "POWER", controller, self.relayButtonHandler)
                self.cluster_node_pwr_buttons[int(pins_df['group'][i])-1].append(button)
                label=LcarsText(colours.WHITE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.label_xpos), name)
                self.cluster_node_labels[pins_df['group'][i]-1].append(label)
                all_sprites.add(label, layer=4)
            else:
                button=RelayResetButton(colours.BLUE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.reset_button_xpos), "RESET", controller, self.relayButtonHandler)
                self.cluster_node_reset_buttons[int(pins_df['group'][i])-1].append(button)
            all_sprites.add(button, layer=4)
            if not int(pins_df['group'][i])==1:
                button.visible=False
                if not label==None:
                    label.visible=False
        
        
        #add background image
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1_modern.png"),
                        layer=0)

        # panel text
        #all_sprites.add(LcarsText(colours.BLUELIGHT, (15, 44), "LCARS 105"),
        #                layer=1)
        self.title_text=LcarsText(colours.WHITE, (10, 135), "CONTROL", 2)                
        all_sprites.add(self.title_text,
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.TRANSPARENT, (145, 16), "CONTROL", self.showControlHandler),
                        layer=1)
        all_sprites.add(LcarsBlockSmall(colours.TRANSPARENT, (211, 16), "SETTINGS", self.showSettingsHandler),
                        layer=1)
        all_sprites.add(LcarsBlockLarge(colours.TRANSPARENT, (249, 16), "STATUS", self.showStatusHandler),
                        layer=1)

        self.ip_address = LcarsText(colours.BLUEDARK, (446, 505),
                                    ":: NODE | "+get_ip_address_string()+" ::", 1.13)
        all_sprites.add(self.ip_address, layer=1)


        # date display
        self.stardate = LcarsText(colours.BLUEMID, (25, 470), "STAR DATE 2311.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons
        all_sprites.add(SideBlockSmall(colours.BLUEMID, (447, 690), "LOGOUT", self.logoutHandler),
                        layer=1)

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()
        
        #ensure only first page displayed
        for sprite in all_sprites.get_sprites_from_layer(5):
            sprite.visible=False
        for sprite in all_sprites.get_sprites_from_layer(6):
            sprite.visible=False
        
        #testing the ultimate button
        #pic1 = pygame.image.load("assets/button_modern.png")
        #pic2 = pygame.image.load("assets/button_modern_down.png")
        #all_sprites.add(UltimateButton((100,100), image_set=[pic1, pic1, pic2], text="hellocd "), layer=4)

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("DATETIME {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            return False

    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def showInfoText(self):
        for sprite in self.info_text:
            sprite.visible = True
        
    def logoutHandler(self, item, event, clock):
        from screens.authorize import ScreenAuthorize
        self.loadScreen(ScreenAuthorize())
        for controller in self.relay_controllers:
            controller.relay.close()
            
    def relayButtonHandler(self, item, event, clock):
        item.relay.dothething()
        
    def clusterButtonHandler(self, item, event, clock):
        #print('running button handler')
        self.hideAllButtons()
        for i in self.cluster_node_labels[item.group_number-1]:
            i.visible=True
        for i in self.cluster_node_pwr_buttons[item.group_number-1]:
            i.visible=True
        for i in self.cluster_node_reset_buttons[item.group_number-1]:
            i.visible=True
            
    def hideAllButtons(self):
        for group in self.cluster_node_pwr_buttons:
            #print(group)
            for i in range(len(group)):
                #print(group[i])
                group[i].visible=False
        for group in self.cluster_node_labels:
            for i in range(len(group)):
                group[i].visible=False
        for group in self.cluster_node_reset_buttons:
            for i in range(len(group)):
                group[i].visible=False
        
    def showControlHandler(self, item, event, clock):
        print('click')
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=False
        for i in self.cluster_buttons:
            i.visible=True
        for i in self.cluster_node_labels[0]:
            i.visible=True
        for i in self.cluster_node_pwr_buttons[0]:
            i.visible=True
        for i in self.cluster_node_reset_buttons[0]:
            i.visible=True
        self.title_text.renderText("CONTROL")
        
        
    def showStatusHandler(self, item, event, clock):
        print('click')
        for sprite in self.all_sprites.get_sprites_from_layer(4):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=True
        self.title_text.renderText("STATUS")
        
    def showSettingsHandler(self, item, event, clock):
        print('click')
        for sprite in self.all_sprites.get_sprites_from_layer(4):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=True
        self.title_text.renderText("SETTINGS")
