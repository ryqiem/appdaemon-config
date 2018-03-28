import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class SingleButton(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

        self.listen_event(self.single_click, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "single")
        self.listen_event(self.double_click, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "double")
        self.listen_event(self.long_click_press, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "long_click_press")

    def single_click(self, entity, attribute, old, new="", kwargs=""):
        if self.get_state("input_select.context") == "Sleep":
            self.log("Toggling night-light for Sleep")

            if self.get_state("light.monitor") == "on":
                self.turn_off("light.monitor")
            elif self.get_state("light.monitor") == "off":
                self.turn_on("light.monitor", xy_color = [0.6948, 0.3002], brightness = "60")

        if self.get_state("input_select.context") == "Pre-sleep":
            self.log("Toggling night-light for Pre-sleep")

            if self.get_state("light.monitor", "brightness") == 60:
                self.turn_on("light.monitor", xy_color = [0.6948, 0.3002], brightness = "150")
            elif self.get_state("light.monitor") != 60:
                self.turn_on("light.monitor", xy_color = [0.6948, 0.3002], brightness = "60")

        if self.get_state("input_select.context") == "Movie-mode":
            self.log("Setting play/pause context")

            if self.get_state("input_select.playing_state") == "playing":
                self.set_state("input_select.playing_state", state = "paused")

            elif self.get_state("input_select.playing_state") == "paused":
                self.set_state("input_select.playing_state", state = "playing")

    def double_click(self, entity, attribute, old, new="", kwargs=""):
        # Define context-specific actions
        self.log("Double-click!")
        if self.get_state("input_select.context") != "Cozy":
            self.set_state("input_select.context", state = "Cozy")
        else:
            self.set_state("input_select.context", state = "Normal")

    def long_click_press(self, entity, attribute, old, new="", kwargs=""):
        self.log("{} turned {}".format(entity, new))
        if self.get_state("input_select.context") != "Pre-sleep":
            self.set_state("input_select.context", state="Pre-sleep")
        else:
            self.set_state("input_select.context", state="Normal")
