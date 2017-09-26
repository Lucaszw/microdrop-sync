from .utils import MicrodropUtils

from os import path


class Device(object):

    def __init__(self, ms):
        self.ms = ms

    def change_dmf_device(self, device_file):
        # Ensure that device_info_plugin is running before loading device:
        if (self.device_info_is_running() is False):
            self.start_device_info_plugin()

        msg = {'name': "dmf_device", 'file': device_file}
        success_topic = MicrodropUtils\
            .get_state_topic('device-model', 'device')
        return self.ms.trigger_sync('device-model', 'put-device', msg,
                                    success_topic=success_topic)

    def find_device_info_plugins(self):
        return self.ms.plugin_manager.find_plugin_by_name("device_info_plugin")

    def device_info_is_running(self):
        return self.ms.plugin_manager\
            .check_status_of_plugin_with_name("device_info_plugin")

    def start_device_info_plugin(self):
        return self.ms.plugin_manager\
            .start_plugin_by_name("device_info_plugin")

    def stop_device_info_plugin(self):
        return self.ms.plugin_manager\
            .stop_plugin_by_name("device_info_plugin")

    def get_from_filelocation(self, url):
        f = open(url, "r")
        return f.read()

    def load_from_filelocation(self, url):
        # Ensure that device_info_plugin is running before loading device:
        if (self.device_info_is_running() is False):
            self.start_device_info_plugin()

        f = self.get_from_filelocation(url)
        msg = {'name': path.splitext(path.basename(url))[0], 'file': f}
        success_topic = MicrodropUtils.get_state_topic('device-model',
                                                       'device')
        return self.ms.trigger_sync('device-model', 'load-device', msg,
                                    success_topic=success_topic)
