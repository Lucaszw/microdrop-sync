from string import Template


class MicrodropUtils():
    def get_plugin_id(name, path):
        return Template('$name:$path').substitute(name=name, path=path)

    def get_signal_topic(sender, topic):
        return Template('microdrop/$sender/signal/$topic').substitute(
            sender=sender, topic=topic)

    def get_state_topic(sender, val):
        return Template('microdrop/$sender/state/$val').substitute(
                        sender=sender, val=val)

    get_plugin_id = staticmethod(get_plugin_id)
    get_signal_topic = staticmethod(get_signal_topic)
    get_state_topic = staticmethod(get_state_topic)
