from .utils import MicrodropUtils as utils


class Protocols(object):

    def __init__(self, ms):
        self.ms = ms
        self.protocols_topic = utils.get_state_topic('protocol-model',
                                                     'protocols')
        self.protocol_skeleton_topic = utils\
            .get_state_topic('protocol-model', 'protocol-skeleton')

    def protocols(self):
        return self.ms.get_state_sync("protocol-model", "protocols")

    def new_protocol(self):
        self.ms.trigger_sync("protocol-model", "new-protocol", {},
                             self.protocols_topic)
        return self.protocols()[-1]

    def current_protocol_skeleton(self):
        return self.ms.get_state_sync("protocol-model", "protocol-skeleton")

    def save_protocol_with_name(self, name):
        return self.ms.trigger_sync("protocol-model", "save-protocol",
                                    {'name': name},
                                    success_topic=self.protocols_topic)

    def load_protocol_with_name(self, name):
        return self.ms.trigger_sync("protocol-model", "change-protocol",
                                    {'name': name},
                                    success_topic=self.protocol_skeleton_topic)

    def delete_protocol_with_name(self, name):
        msg = {'protocol': {'name': name}}
        return self.ms.trigger_sync("protocol-model", "delete-protocol", msg,
                                    success_topic=self.protocols_topic)

    def upload_protocol(self, protocol):
        msg = {'protocol': protocol}
        return self.ms.trigger_sync("protocol-model", "upload-protocol", msg,
                                    success_topic=self.protocols_topic)
