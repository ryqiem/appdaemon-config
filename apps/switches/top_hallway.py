import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
import globals as g

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

# Button C

class TopHallway(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

        self.listen_event(self.single_click, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a24c", click_type = "single")
        self.listen_event(self.double_click, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a24c", click_type = "double")
        self.listen_event(self.long_click_press, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a24c", click_type = "long_click_press")

        self.Utils = self.get_app("Utilities")

    def single_click(self, entity, attribute, old, new="", kwargs=""):
        if self.get_state("input_select.context") != "Away":
            self.set_state("input_select.context", state = "Away")
        else:
            g.door_opened_recently = 1
            self.set_state("input_select.context", state = "Normal")

    def double_click(self, entity, attribute, old, new="", kwargs=""):
        # Define context-specific actions
        self.log("Double-click!")

    def long_click_press(self, entity, attribute, old, new="", kwargs=""):
        self.log("{} turned {}".format(entity, new))
        if g.c_colortemp == 2000 and g.c_brightness == 655 and g.persistent_hallway_light == True:
            self.set_state("input_select.context", state="Normal")
            self.Utils.light_setter(lt="light.gang",
                          brightness=655,
                          fade=1)
        else:
            if self.get_state("light.gang") == "on":
                self.turn_off("light.gang")
            else:
                self.Utils.light_setter(lt="light.gang", fade=1)
