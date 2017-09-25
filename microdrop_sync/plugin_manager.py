from .utils import MicrodropUtils


class PluginManager(object):

    def __init__(self, ms):
        self.ms = ms

    def add_plugin_path(self, path):
        success_topic = MicrodropUtils.get_state_topic("web-server",
                                                       "process-plugins")
        var = {}
        var['path'] = path
        return self.ms.trigger_sync("web-server", "add-plugin-path",
                                    var, success_topic)

    def disable_web_plugin(self, path):
        plugin = self.get_web_plugins()[path]
        success_topic = MicrodropUtils.get_state_topic('web-server',
                                                       'web-plugins')
        if (plugin['state'] == 'disabled'):
            return False

        plugin['state'] = 'disabled'
        return self.ms.trigger_sync("web-server", "update-ui-plugin-state",
                                    plugin, success_topic)[path]

    def enable_web_plugin(self, path):
        plugin = self.get_web_plugins()[path]
        success_topic = MicrodropUtils.get_state_topic('web-server',
                                                       'web-plugins')
        if (plugin['state'] == 'enabled'):
            return False

        plugin['state'] = 'enabled'
        return self.ms.trigger_sync("web-server", "update-ui-plugin-state",
                                    plugin, success_topic)[path]

    def get_process_plugins(self):
        return self.ms.get_state_sync("web-server", "process-plugins")

    def get_running_process_plugins(self):
        plugins = self.get_process_plugins()
        running_plugins = []
        for id, plugin in plugins.iteritems():
            if (plugin['state'] == 'running'):
                running_plugins.append(plugin)
        return running_plugins

    def get_web_plugins(self):
        return self.ms.get_state_sync("web-server", "web-plugins")

    def remove_plugin_path(self, path):
        successTopic = MicrodropUtils.get_state_topic("web-server",
                                                      "process-plugins")
        var = {}
        var['path'] = path
        return self.ms.trigger_sync("web-server", "remove-plugin-path",
                                    var, successTopic)

    def start_process_plugin(self, id):
        # Get Process Plugins:
        plugin = self.get_process_plugins()[id]

        success_topic = MicrodropUtils.get_signal_topic(plugin['name'],
                                                        'running')
        if (plugin['state'] == 'running'):
            return False
        self.ms.trigger_sync("web-server", "launch-plugin",
                             plugin['path'], success_topic)
        return self.get_process_plugins()[id]

    def stop_process_plugin(self, id):
        process_plugins = self.get_process_plugins()
        plugin = process_plugins[id]
        if (plugin['state'] == 'stopped'):
            return False

        success_topic = MicrodropUtils.get_signal_topic("broker",
                                                        'client-disconnected')
        self.ms.trigger_sync("web-server", "close-plugin",
                             plugin['name'], success_topic)
        # TODO: Validate the client name matches the plugin that was closed
        return self.get_process_plugins()[id]
