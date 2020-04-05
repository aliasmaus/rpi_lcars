from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen

from controllers.relaycontroller import relaycontroller as RC

from datasources.network import get_ip_address_string
import pandas as pd

class ScreenMain(LcarsScreen):
    relaycontrollers=[]
    label_xpos=140
    pwr_button_xpos=200
    reset_button_xpos=300
    cluster_button_xpos=140
    cluster_button_ypos=120
    cluster_button_xinterval=140
    content_ypos=180
    content_yinterval=60
    cluster_node_labels=[]
    cluster_node_pwr_buttons=[]
    cluster_node_reset_buttons=[]

    def setup(self, all_sprites):
        #relay setup
        pins_df=pd.read_csv("data/buttons.csv")
        print(pins_df.head())
        for i in range(pins_df['group'].max()):
            all_sprites.add(LcarsButton(colours.BEIGE, (self.cluster_button_ypos, self.cluster_button_xpos+(self.cluster_button_xinterval*i)), "TOWER "+ str(i+1), self.sensorsHandler),
                        layer=4)
            self.cluster_node_labels.append([])
            self.cluster_node_pwr_buttons.append([])
            self.cluster_node_reset_buttons.append([])
        for i in range(len(pins_df)):
            if pins_df['type'][i]=='power':
                self.cluster_node_pwr_buttons[int(pins_df['group'][i])-1].append(all_sprites.add(LcarsButton(colours.BEIGE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.pwr_button_xpos), "POWER", self.sensorsHandler),
                            layer=4))
            else:
                self.cluster_node_reset_buttons[int(pins_df['group'][i])-1].append(all_sprites.add(LcarsButton(colours.BEIGE, (self.content_ypos+(self.content_yinterval*(int(pins_df['computer_number'][i])-1)), self.reset_button_xpos), "RESET", self.sensorsHandler, rectSize=(80,40)),
                            layer=4))
            self.relaycontrollers.append(RC(int(pins_df['gpio_pin'][i])))

        print(str(self.cluster_node_pwr_buttons))

        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1b.png"),
                        layer=0)

        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "LCARS 105"),
                        layer=1)
                        
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "CLUSTER MASTER 3000", 2),
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "CONTROL"),
                        layer=1)
        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "STATUS"),
                        layer=1)
        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "SETTINGS"),
                        layer=1)

        self.ip_address = LcarsText(colours.BLACK, (444, 520),
                                    get_ip_address_string())
        all_sprites.add(self.ip_address, layer=1)

        # info text
        #all_sprites.add(LcarsText(colours.WHITE, (192, 174), "EVENT LOG:", 1.5),
        #                layer=3)
        #all_sprites.add(LcarsText(colours.BLUE, (244, 174), "2 ALARM ZONES TRIGGERED", 1.5),
        #                layer=3)
        #all_sprites.add(LcarsText(colours.BLUE, (286, 174), "14.3 kWh USED YESTERDAY", 1.5),
        #                layer=3)
        #all_sprites.add(LcarsText(colours.BLUE, (330, 174), "1.3 Tb DATA USED THIS MONTH", 1.5),
        #                layer=3)
        #self.info_text = all_sprites.get_sprites_from_layer(3)
        
        #on/off/reset button test
        #all_sprites.add(RelayButton(colours.RED_BROWN, (192, 174), str(pins_df.iloc[i,4]), self.testrelayhandler,relaycontrollers[i]),
         #               layer=3)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 400), "STAR DATE 2311.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons
        #all_sprites.add(LcarsButton(colours.RED_BROWN, (6, 662), "LOGOUT", self.logoutHandler),
        #                layer=4)
        #all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "TOWER 1", self.sensorsHandler),
        #                layer=4)
        #all_sprites.add(LcarsButton(colours.PURPLE, (107, 262), "TOWER 2", self.gaugesHandler),
        #                layer=4)
        #all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "RPi TOWER 1", self.weatherHandler),
        #                layer=4)
        #all_sprites.add(LcarsButton(colours.PEACH, (108, 536), "RPi TOWER 2", self.homeHandler),
        #                layer=4)

        # gadgets
        all_sprites.add(LcarsGifImage("assets/gadgets/fwscan.gif", (277, 556), 100), layer=1)

        self.sensor_gadget = LcarsGifImage("assets/gadgets/lcars_anim2.gif", (235, 150), 100)
        self.sensor_gadget.visible = False
        all_sprites.add(self.sensor_gadget, layer=2)

        self.dashboard = LcarsImage("assets/gadgets/dashboard.png", (187, 232))
        self.dashboard.visible = False
        all_sprites.add(self.dashboard, layer=2)

        self.weather = LcarsImage("assets/weather.jpg", (188, 122))
        self.weather.visible = False
        all_sprites.add(self.weather, layer=2)

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
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

    def gaugesHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = True
        self.weather.visible = False

    def sensorsHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = True
        self.dashboard.visible = False
        self.weather.visible = False

    def weatherHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.weather.visible = True

    def homeHandler(self, item, event, clock):
        self.showInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.weather.visible = False
        
    def logoutHandler(self, item, event, clock):
        from screens.authorize import ScreenAuthorize
        self.loadScreen(ScreenAuthorize())
        
    def testrelayhandler(self, item, event, clock):
        self.relaycontrollers[0].dothething()


