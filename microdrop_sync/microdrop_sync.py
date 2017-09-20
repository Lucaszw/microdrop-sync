import paho_mqtt_helpers as pmh

from .plugin_manager import PluginManager


class MicrodropSync(pmh.BaseMqttReactor):

    def __init__(self, *args, **kwargs):
        self.name = self.plugin_name
        pmh.BaseMqttReactor.__init__(self)
        self.start()
        self.plugin_manager = PluginManager(self)

    def getStateSync(self, sender, val):
        """ Blocking method to directly get state variable"""
        variables = {}
        variables['notSet'] = True
        variables['output'] = None

        def onVariableSet(x, a):
            variables['notSet'] = False
            variables['output'] = x

        sub = self.onStateMsg(sender, val, onVariableSet)

        self.mqtt_client.subscribe(sub)

        while variables['notSet']:
            pass

        return variables['output']

    def triggerSync(self, receiver, action, val, successTopic=None):
        var = {}
        var['messageNotDelivered'] = True
        var['output'] = True
        callback = self.bindTriggerMsg(receiver, action, "trigger-event")

        def onSuccess(payload, args):
            var['messageNotDelivered'] = False
            var['output'] = payload

        self.trigger("trigger-event", val)

        if successTopic:
            sub = self.addSubscription(successTopic, onSuccess)
            self.mqtt_client.subscribe(sub)
            while var['messageNotDelivered']:
                pass

        self.off("trigger-event", callback)

        return var['output']
