from .utils import MicrodropUtils


class PluginManager(object):

    def __init__(self, ms):
        self.ms = ms

    def addPluginPath(self, path):
        successTopic = MicrodropUtils.getStateTopic("web-server",
                                                    "process-plugins")
        var = {}
        var['path'] = path
        return self.ms.triggerSync("web-server", "add-plugin-path",
                                   var, successTopic)

    def removePluginPath(self, path):
        successTopic = MicrodropUtils.getStateTopic("web-server",
                                                    "process-plugins")
        var = {}
        var['path'] = path
        return self.ms.triggerSync("web-server", "remove-plugin-path",
                                   var, successTopic)

    def getProcessPlugins(self):
        return self.ms.getStateSync("web-server", "process-plugins")

    def getWebPlugins(self):
        return self.ms.getStateSync("web-server", "web-plugins")

    def enableWebPlugin(self, path):
        plugin = self.getWebPlugins()[path]
        successTopic = MicrodropUtils.getStateTopic('web-server',
                                                    'web-plugins')
        if (plugin['state'] == 'enabled'):
            return False

        plugin['state'] = 'enabled'
        return self.ms.triggerSync("web-server", "update-ui-plugin-state",
                                   plugin, successTopic)[path]

    def disableWebPlugin(self, path):
        plugin = self.getWebPlugins()[path]
        successTopic = MicrodropUtils.getStateTopic('web-server',
                                                    'web-plugins')
        if (plugin['state'] == 'disabled'):
            return False

        plugin['state'] = 'disabled'
        return self.ms.triggerSync("web-server", "update-ui-plugin-state",
                                   plugin, successTopic)[path]

    def startProcessPlugin(self, id):
        # Get Process Plugins:
        plugin = self.getProcessPlugins()[id]

        successTopic = MicrodropUtils.getSignalTopic(plugin['name'],
                                                     'plugin-started')
        if (plugin['state'] == 'running'):
            return False
        self.ms.triggerSync("web-server", "launch-plugin",
                            plugin['path'], successTopic)
        return self.getProcessPlugins()[id]

    def stopProcessPlugin(self, id):
        process_plugins = self.getProcessPlugins()
        plugin = process_plugins[id]
        if (plugin['state'] == 'stopped'):
            return False
        successTopic = MicrodropUtils.getSignalTopic(plugin['name'],
                                                     'plugin-exited')
        self.ms.triggerSync("web-server", "close-plugin",
                            plugin['name'], successTopic)
        return self.getProcessPlugins()[id]
