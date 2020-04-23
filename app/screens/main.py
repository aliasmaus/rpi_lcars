from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen

from controllers.relaycontroller import relaycontroller as RC
from components.clusternode import ClusterNode as CN

from datasources.network import get_ip_address_string
import pandas as pd
import gpiozero

class ScreenMain(LcarsScreen):
    #DEFAULTS
    label_xpos=150
    pwr_button_xpos=730
    reset_button_xpos=680
    content_ypos=140
    content_yinterval=70
    title_text=None
    button_image=pygame.image.load("assets/button.png")

    #COMPONENT ARRAYS
    nodes=[]
    status_labels=[]
    cluster_node_labels=[]
    cluster_node_pwr_buttons=[]
    cluster_node_reset_buttons=[]
    relay_controllers=[]
    cluster_buttons=[]
    bank_number=1
    visible_layer=4
    
    nextScreen=None
    
    def __init__(self):
        pins_df=pd.read_csv("data/buttons.csv")
        #loop through each relay in the config file (data/buttons.csv) and spawn a relay controller
        for i in range(len(pins_df)):
            button=None
            label=None
            print(str(pins_df['ip_address'][i]))
            #local controllers
            if not str(pins_df['ip_address'][i]).startswith("192"):
                controller=RC(int(pins_df['gpio_pin'][i]))
            #remote gpio
            else:
                controller=RC(int(pins_df['gpio_pin'][i]), remotehost=str(pins_df['ip_address'][i]))
            
            self.relay_controllers.append(controller)
            if pins_df['type'][i]=='power':
                self.nodes.append(CN('192.168.1.'+pins_df['node_ip_suffix'][i]))

    def setup(self, all_sprites):
        #relay setup
        # get configuration from file
        pins_df=pd.read_csv("data/buttons.csv")
        self.all_sprites=all_sprites
        
        self.total_banks=pins_df['group'].max()
        #loop through each cluster
        for i in range(pins_df['group'].max()):
            #create arrays for labels, power/reset buttons
            self.cluster_node_labels.append([])
            self.cluster_node_pwr_buttons.append([])
            self.cluster_node_reset_buttons.append([])
            self.status_labels.append([])
        
        #Elbow up-down buttons
        all_sprites.add(ModernElbowTop(colours.TRANSPARENT, (77,15), "", handler=self.changeClusterUp), layer=1)
        all_sprites.add(ModernElbowBottom(colours.TRANSPARENT, (400,15), "", handler=self.changeClusterDown), layer=1)

        for i in range(len(pins_df)):
            button=None
            label=None
            controller=self.relay_controllers[i]

            #create relevant button and add it to all_sprites and button array
            #buttons not in group 1 hidden by default
            #labels are created at same time as power buttons
            if pins_df['type'][i]=='power':
                name=pins_df['name'][i]
                button=RelayPowerButton(colours.PURPLE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.pwr_button_xpos), "POWER", controller, self.relayButtonHandler)
                self.cluster_node_pwr_buttons[int(pins_df['group'][i])-1].append(button)
                label=DescText(colours.WHITE, ((self.content_ypos+5)+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.label_xpos), name)
                statuslabel=DescText(colours.RED, (self.content_ypos+5)+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)+20, self.label_xpos), "OFFLINE")
                self.cluster_node_labels[pins_df['group'][i]-1].append(label)
                self.status_labels[pins_df['group'][i]-1].append(statuslabel)
                all_sprites.add(label, layer=4)
                all_sprites.add(statuslabel, layer=4)
                print(nodes[i-((pins_df['group'][i]-1)*4)].ip_address)
                #nodes[i-((pins_df['group'][i]-1)*4)].statuslabel=statuslabel

            #create reset buttons
            else:
                button=RelayResetButton(colours.WHITE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.reset_button_xpos), "RESET", controller, self.relayButtonHandler)
                self.cluster_node_reset_buttons[int(pins_df['group'][i])-1].append(button)
            all_sprites.add(button, layer=4)

            #set buttons not in group to not be visible
            if not int(pins_df['group'][i])==1:
                button.visible=False
                statuslabel.Visible=False
                if not label==None:
                    label.visible=False
        
        
        # background image
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1_modern.png"),
                        layer=0)

        # panel text
        #all_sprites.add(YukonText(colours.BLUEDARK, (117, 90), "UP"),
        #                layer=1)
        #all_sprites.add(YukonText(colours.BLUEDARK, (420, 65), "dOWN"),
        #                layer=1)
        self.title_text=LcarsText(colours.WHITE, (10, 135), "CLUSTER CONTROL", 2)                
        all_sprites.add(self.title_text,
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.TRANSPARENT, (145, 16), "CONTROL", self.showControlHandler),
                        layer=1)
        all_sprites.add(LcarsBlockSmall(colours.WHITE, (211, 16), "STATUS", self.showStatusHandler),
                        layer=1)
        all_sprites.add(LcarsBlockLarge(colours.WHITE, (249, 16), "SETTINGS", self.showSettingsHandler),
                        layer=1)

        self.ip_address = LcarsText(colours.BLUEDARK, (446, 505),
                                    ":: NODE | "+get_ip_address_string()+" ::", 1.13)
        all_sprites.add(self.ip_address, layer=1)
        
        self.bank_number_text = LcarsText(colours.BLUEDARK, (79, 331),
                                    "BANK   "+str(self.bank_number), 1.1)
        all_sprites.add(self.bank_number_text, layer=1)

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
        self.loadScreen(ScreenAuthorize(), params={self})
        #for controller in self.relay_controllers:
        #    controller.relay.close()

    def relayButtonHandler(self, item, event, clock):
        item.relay.dothething()
        pass
        
    def clusterButtonHandler(self, item, event, clock):
        #print('running button handler')
        self.hideAllButtons()
        for i in self.cluster_node_labels[item.group_number-1]:
            i.visible=True
        for i in self.cluster_node_pwr_buttons[item.group_number-1]:
            i.visible=True
        for i in self.cluster_node_reset_buttons[item.group_number-1]:
            i.visible=True

    def changeClusterUp(self, item, event, clock):
        self.bank_number -= 1
        if self.bank_number <= 0:
            self.bank_number = self.total_banks
        layer=self.visible_layer
        if layer == 4:
            self.hideAllButtons()
            self.showLayerFour(self.bank_number)
        self.bank_number_text.renderText("BANK   "+str(self.bank_number))

    def changeClusterDown(self, item, event, clock):
        self.bank_number += 1
        if self.bank_number > self.total_banks:
            self.bank_number = 1 
        layer=self.visible_layer
        if layer == 4:
            self.hideAllButtons()
            self.showLayerFour(self.bank_number)
        self.bank_number_text.renderText("BANK   "+str(self.bank_number))
        

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
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=False
        #for i in self.cluster_buttons:
        #    i.visible=True
        self.showLayerFour(self.bank_number)
        self.title_text.renderText("CLUSTER CONTROL")
        self.visible_layer=4

    def showLayerFour(self, bank):
        for i in self.cluster_node_labels[bank-1]:
            i.visible=True
        for i in self.cluster_node_pwr_buttons[bank-1]:
            i.visible=True
        for i in self.cluster_node_reset_buttons[bank-1]:
            i.visible=True
        for i in self.status_labels[bank-1]:
            i.visible=True
            
    def showStatusHandler(self, item, event, clock):
        for sprite in self.all_sprites.get_sprites_from_layer(4):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=False
        #will need updating when features added
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=True
        self.title_text.renderText("CLUSTER STATUS")
        self.visible_layer=5
        
    def showSettingsHandler(self, item, event, clock):
        for sprite in self.all_sprites.get_sprites_from_layer(4):
            sprite.visible=False
        for sprite in self.all_sprites.get_sprites_from_layer(5):
            sprite.visible=False
        #will need updating when features added
        for sprite in self.all_sprites.get_sprites_from_layer(6):
            sprite.visible=True
        self.title_text.renderText("APP SETTINGS")
        self.visible_layer=6
