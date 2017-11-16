import appdaemon.appapi as appapi
import time
#
# Presence light
#
# Args:
#
# light: which main light to turn on momentarily when someone arrives
# delay: number of seconds to wait before switching off light

class PresenceLight(appapi.AppDaemon):

    def initialize(self):
        self.log('Available trackers')
        self.light = 'light.soffa' # Color bulb that will change depending on who gets home
        trackers = self.get_trackers()
        for tracker in trackers:
            self.log("{} ({}) is {}".format(self.friendly_name(tracker), tracker, self.get_tracker_state(tracker)))
        self.listen_state(self.presence_change, "device_tracker")
       
    def presence_change(self, tracker, attribute, old, new, kwargs):
        self.log('Tracker: {}, attribute: {}, old: {}, new: {}'.format(tracker, attribute, old, new))
        if old != new:
#            self.log('State change: {} -> {}'.format(old, new))
            if new == 'home':
                self.someone_has_arrived(tracker)
    
    def someone_has_arrived(self, tracker):
        self.log('{} has arrived home'.format(self.friendly_name(tracker)))
        self.turn_on_light(self.args['light'], self.args['delay'])
        self.color_light(tracker)
    
    def turn_on_light(self, light, delay):
        self.log('Turn on {} for {} seconds'.format(light, delay))
        self.turn_on(light)
        handle = self.run_in(self.turn_off_light, delay, light=light)
    
    def turn_off_light(self, kwargs):
        light = kwargs['light']
        self.log('Turn off {}'.format(light))
        self.turn_off(light)
    
    def color_light(self, tracker):
        colors = {'Linda':'red', 'Niklas':'blue', 'Olle':'purple', 'Disa':'green'}
        person = self.friendly_name(tracker)
        self.log('{} is home, set {} to {}'.format(person, self.light, colors[person]))
        self.get_original_values() 
        # set to person color and max brightness
        self.turn_on(self.light, color_name=colors[person], brightness=254, transition=1)
        # set to original rgb_color and brightness after 5 seconds
        handle = self.run_in(self.reset_light, 5)

    def get_original_values(self):
        self.state = self.get_state(self.light)
        # Turn on and save the rgb_color and brightness (not available if light was off)
        self.turn_on(self.light)
        # Need a delay otherwise values are still not available
        # Using time.sleep although documentation recommends against it.
        # See https://github.com/home-assistant/appdaemon/issues/26
        time.sleep(0.1)
        self.rgb = self.get_state(self.light, 'rgb_color')
        self.brightness = self.get_state(self.light, 'brightness')
        self.log('Original values: {}, RGB: {}, brightness: {}'.format(self.state, self.rgb, self.brightness), level="DEBUG")

    def reset_light(self, kwargs):
        self.log('Reset {} to {}, brightness: {}'.format(self.light, self.rgb, self.brightness))
        self.turn_on(self.light, rgb_color=self.rgb, brightness=self.brightness, transition=1)
        # turn off if it was off before
        if self.state == 'off':
            self.turn_off(self.light)
