from .utils import MicrodropUtils

from os import path


class Device(object):

    def __init__(self, ms):
        self.ms = ms

    def change_dmf_device(self, device_file):
        # Ensure that device_info_plugin is running before loading device:
        if (self.device_info_is_running() is False):
            self.start_device_info_plugin()

        msg = {
            'name': "dmf_device",
            'file': device_file
        }
        success_topic = MicrodropUtils.get_state_topic('device-model',
                                                       'device')
        return self.ms.trigger_sync('device-model', 'put-device', msg,
                                    success_topic=success_topic)

    def find_device_info_plugins(self):
        plugins = self.ms.plugin_manager.get_process_plugins()
        device_info_plugins = []
        for id, plugin in plugins.iteritems():
            if plugin['name'] == 'device_info_plugin':
                device_info_plugins.append(plugin)
        return device_info_plugins

    def device_info_is_running(self):
        device_info_plugins = self.find_device_info_plugins()
        running_state = False
        for plugin in device_info_plugins:
            if plugin['state'] == "running":
                running_state = True
        return running_state

    def start_device_info_plugin(self):
        device_info_plugins = self.find_device_info_plugins()
        if (len(device_info_plugins) == 0):
            raise RuntimeError("Could not find device_info_plugin. \n"
                               "Have you added device_info_plugin to the"
                               "plugin manager?")

        for plugin in device_info_plugins:
            if plugin['state'] == "stopped":
                plugin_id = plugin['name'] + ":" + plugin['path']
                self.ms.plugin_manager.start_process_plugin(plugin_id)
                return self.find_device_info_plugins()

        return self.find_device_info_plugins()

    def stop_device_info_plugin(self):
        device_info_plugins = self.find_device_info_plugins()
        for plugin in device_info_plugins:
            if plugin['state'] == "running":
                plugin_id = plugin['name'] + ":" + plugin['path']
                self.ms.plugin_manager.stop_process_plugin(plugin_id)
        return self.find_device_info_plugins()

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
