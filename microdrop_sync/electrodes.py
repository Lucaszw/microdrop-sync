from .utils import MicrodropUtils


class Electrodes(object):

    def __init__(self, ms):
        self.ms = ms

    def get_electrodes(self):
        return self.ms.get_state_sync("electrodes-model", "electrodes")

    def get_channels(self):
        return self.ms.get_state_sync("electrodes-model", "channels")

    def get_on_electrodes(self):
        all_electrodes = self.ms.get_state_sync("electrodes-model",
                                                "electrodes")
        on_electrodes = []
        for electrode_id, state in all_electrodes.iteritems():
            if state is True:
                on_electrodes.append(electrode_id)
        return on_electrodes

    def turn_off_electrode(self, electrode_id):
        msg = {}
        msg['electrode_id'] = electrode_id
        msg['state'] = False

        success_topic = MicrodropUtils.get_state_topic('electrodes-model',
                                                       'electrodes')
        return self.ms.put_sync('electrodes-model', 'electrode-state',
                                msg, success_topic)[electrode_id]

    def turn_on_electrode(self, electrode_id):
        msg = {}
        msg['electrode_id'] = electrode_id
        msg['state'] = True

        success_topic = MicrodropUtils.get_state_topic('electrodes-model',
                                                       'electrodes')
        return self.ms.put_sync('electrodes-model', 'electrode-state',
                                msg, success_topic)[electrode_id]

    def turn_on_electrodes(self, electrode_ids):
        for electrode_id in electrode_ids:
            self.turn_on_electrode(electrode_id)
        return self.get_on_electrodes()

    def turn_off_electrodes(self, electrode_ids):
        for electrode_id in electrode_ids:
            self.turn_off_electrode(electrode_id)
        return self.get_on_electrodes()

    def clear_electrodes(self):
        all_electrodes = self.ms.get_state_sync("electrodes-model",
                                                "electrodes")
        for electrode_id, state in all_electrodes.iteritems():
            if state is True:
                self.turn_off_electrode(electrode_id)
        return self.get_on_electrodes()
