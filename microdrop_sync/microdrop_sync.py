import threading

import paho_mqtt_helpers as pmh

from .device import Device
from .electrodes import Electrodes
from .plugin_manager import PluginManager


class MicrodropSync(pmh.BaseMqttReactor):

    def __init__(self, *args, **kwargs):
        self.name = self.plugin_name
        pmh.BaseMqttReactor.__init__(self)
        self.start()
        self.plugin_manager = PluginManager(self)
        self.device = Device(self)
        self.electrodes = Electrodes(self)
        self.default_timeout = 5.0

    def start(self):
        # Connect to MQTT broker.
        self._connect()
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        pass

    def put_sync(self, receiver, prop, val, success_topic=None):
        callback = self.bindPutMsg(receiver, prop, "trigger-event")
        return self.broadcast_sync(callback, "trigger-event", val,
                                   success_topic)

    def trigger_sync(self, receiver, action, val, success_topic=None):
        callback = self.bindTriggerMsg(receiver, action, "trigger-event")
        return self.broadcast_sync(callback, "trigger-event", val,
                                   success_topic)

    def get_state_sync(self, sender, val):
        """ Blocking method to directly get state variable"""
        var = {}
        var['notSet'] = True
        var['output'] = None
        var['status'] = "MESSAGE PENDING"

        def on_variable_set(x, a):
            if var['notSet']:
                var['output'] = x
                var['status'] = "SUCCESS"
                var['notSet'] = False

        def on_timeout():
            if var['notSet']:
                var['messageNotDelivered'] = False
                var['status'] = "MAX TIMEOUT ERROR"

        var['sub'] = self.onStateMsg(sender, val, on_variable_set)
        self.mqtt_client.subscribe(var['sub'])
        t = threading.Timer(self.default_timeout, on_timeout)
        t.start()
        while var['notSet']:
            pass

        if var['status'] == "SUCCESS":
            return var['output']
        else:
            raise RuntimeError(var['status'] + "\n" +
                               sender)

    def broadcast_sync(self, callback, event, val, success_topic=None):
        var = {}
        var['messageNotDelivered'] = True
        var['output'] = None
        var['status'] = "MESSAGE PENDING"

        def on_success(payload, args):
            if var['messageNotDelivered']:
                var['output'] = payload
                var['status'] = "SUCCESS"
                var['messageNotDelivered'] = False

        def on_timeout():
            if var['messageNotDelivered']:
                var['messageNotDelivered'] = False
                var['status'] = "MAX TIMEOUT ERROR"

        self.trigger("trigger-event", val)

        if success_topic:
            var['sub'] = self.addSubscription(success_topic, on_success)
            self.mqtt_client.subscribe(var['sub'])
            t = threading.Timer(self.default_timeout, on_timeout)
            t.start()
            while var['messageNotDelivered']:
                pass
        else:
            var['status'] = "SUCCESS"

        if var['status'] == "SUCCESS":
            self.off("trigger-event", callback)
            return var['output']
        else:
            raise RuntimeError(var['status'] + "\n" +
                               success_topic)
