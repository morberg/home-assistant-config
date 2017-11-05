import appdaemon.appapi as appapi

#
# Presence light
#
# Args:
#
# light: which main light to turn on momentarily when someone arrives
# delay: number of seconds to wait before switching off light

class PresenceLight(appapi.AppDaemon):

    def initialize(self):
        trackers = self.get_trackers()
        self.log('Available trackers')
        for tracker in trackers:
            self.log("{} ({}) is {}".format(self.friendly_name(tracker), tracker, self.get_tracker_state(tracker)))
        self.listen_state(self.presence_change, "device_tracker")
       
    def presence_change(self, tracker, attribute, old, new, kwargs):
        self.log('Tracker: {}, attribute: {}, old: {}, new: {}'.format(tracker, attribute, old, new))
        if old != new:
            self.log('State change: {} -> {}'.format(old, new))
            if new == 'home':
                self.someone_has_arrived(tracker)
    
    def someone_has_arrived(self, tracker):
        self.log('{} has arrived home'.format(self.friendly_name(tracker)))
        self.turn_on_light(self.args['light'], self.args['delay'])
    
    def turn_on_light(self, light, delay):
        self.log('Turn on {} for {} seconds'.format(light, delay))
        self.turn_on(light)
        handle = self.run_in(self.turn_off_light, delay, light=light)
    
    def turn_off_light(self, kwargs):
        light = kwargs['light']
        self.log('Turn off {}'.format(light))
        self.turn_off(light)