from string import Template


class MicrodropUtils():
    def getPluginId(name, path):
        return Template('$name:$path').substitute(name=name, path=path)

    def getSignalTopic(sender, topic):
        return Template('microdrop/$sender/signal/$topic').substitute(
            sender=sender, topic=topic)

    def getStateTopic(sender, val):
        return Template('microdrop/$sender/state/$val').substitute(
                        sender=sender, val=val)

    getPluginId = staticmethod(getPluginId)
    getSignalTopic = staticmethod(getSignalTopic)
    getStateTopic = staticmethod(getStateTopic)
