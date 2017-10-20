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
        successTopic = MicrodropUtils\
            .get_state_topic("web-server", "process-plugins")
        var = {}
        var['path'] = path
        return self.ms.trigger_sync("web-server", "remove-plugin-path",
                                    var, successTopic)

    def start_process_plugin(self, id):
        print ("start_process_plugin depricated.")
        print ("use start_process_plugin_by_id instead")
        return self.start_process_plugin_by_id(id)

    def start_process_plugin_by_id(self, id):
        plugin = self.get_process_plugins()[id]
        success_topic = MicrodropUtils\
            .get_signal_topic(plugin['name'], 'running')
        if (plugin['state'] == 'running'):
            return False
        self.ms.trigger_sync("web-server", "launch-plugin",
                             plugin['path'], success_topic)
        return self.get_process_plugins()[id]

    def find_plugin_by_name(self, name):
        plugins = self.get_process_plugins()
        plugin_instances = []
        for id, plugin in plugins.iteritems():
            if plugin['name'] == name:
                plugin_instances.append(plugin)
        return plugin_instances

    def check_status_of_plugin_with_name(self, name):
        plugin_instances = self.find_plugin_by_name(name)
        running_state = False
        for plugin in plugin_instances:
            if plugin['state'] == "running":
                running_state = True
        return running_state

    def start_plugin_by_name(self, name):
        plugin_instances = self.find_plugin_by_name(name)
        running_state = self.check_status_of_plugin_with_name(name)
        if (running_state is True):
            print("PLUGIN ALREADY RUNNING: " + name)
            return
        if (len(plugin_instances) > 1):
            print("WARNING: MORE THAN ONE INSTANCE OF " + name)
            print("Recommend starting plugin by id vs. name")
        if (len(plugin_instances) == 0):
            raise RuntimeError("Could not find " + name + "\n"
                               "Have you added " + name + " to the"
                               "plugin manager?")
        for plugin in plugin_instances:
            if plugin['state'] == "stopped":
                plugin_id = plugin['name'] + ":" + plugin['path']
                self.start_process_plugin(plugin_id)
                return self.find_plugin_by_name(name)
        return self.find_plugin_by_name(name)

    def stop_plugin_by_name(self, name):
        plugin_instances = self.find_plugin_by_name(name)
        running_state = self.check_status_of_plugin_with_name(name)
        if (running_state is False):
            print("PLUGIN ALREADY STOPPED: " + name)
            return
        if (len(plugin_instances) == 0):
            raise RuntimeError("Could not find " + name + "\n"
                               "Have you added " + name + " to the"
                               "plugin manager?")
        for plugin in plugin_instances:
            if plugin['state'] == "running":
                plugin_id = plugin['name'] + ":" + plugin['path']
                self.stop_process_plugin(plugin_id)
        return self.find_plugin_by_name(name)

    def stop_process_plugin(self, id):
        process_plugins = self.get_process_plugins()
        plugin = process_plugins[id]
        if (plugin['state'] == 'stopped'):
            return False
        success_topic = MicrodropUtils\
            .get_signal_topic("broker", 'client-disconnected')
        self.ms.trigger_sync("web-server", "close-plugin", plugin['name'],
                             success_topic)
        # TODO: Validate the client name matches the plugin that was closed
        return self.get_process_plugins()[id]
