import paho_mqtt_helpers as pmh

from .electrodes import Electrodes
from .plugin_manager import PluginManager


class MicrodropSync(pmh.BaseMqttReactor):

    def __init__(self, *args, **kwargs):
        self.name = self.plugin_name
        pmh.BaseMqttReactor.__init__(self)
        self.start()
        self.plugin_manager = PluginManager(self)
        self.electrodes = Electrodes(self)

    def start(self):
        # Connect to MQTT broker.
        self._connect()
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        pass

    def get_state_sync(self, sender, val):
        """ Blocking method to directly get state variable"""
        variables = {}
        variables['notSet'] = True
        variables['output'] = None

        def on_variable_set(x, a):
            variables['notSet'] = False
            variables['output'] = x

        sub = self.onStateMsg(sender, val, on_variable_set)

        self.mqtt_client.subscribe(sub)

        while variables['notSet']:
            pass

        return variables['output']

    def put_sync(self, receiver, prop, val, success_topic=None):
        callback = self.bindPutMsg(receiver, prop, "trigger-event")
        return self.broadcast_sync(callback, "trigger-event", val,
                                   success_topic)

    def trigger_sync(self, receiver, action, val, success_topic=None):
        callback = self.bindTriggerMsg(receiver, action, "trigger-event")
        return self.broadcast_sync(callback, "trigger-event", val,
                                   success_topic)

    def broadcast_sync(self, callback, event, val, success_topic=None):
        var = {}
        var['messageNotDelivered'] = True
        var['output'] = None

        def on_success(payload, args):
            var['messageNotDelivered'] = False
            var['output'] = payload

        self.trigger("trigger-event", val)

        if success_topic:
            sub = self.addSubscription(success_topic, on_success)
            self.mqtt_client.subscribe(sub)
            while var['messageNotDelivered']:
                pass

        self.off("trigger-event", callback)

        return var['output']
