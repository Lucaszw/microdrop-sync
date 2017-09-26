from .utils import MicrodropUtils


class Routes(object):

    def __init__(self, ms):
        self.ms = ms

    def droplet_planning_is_running(self):
        return self.ms.plugin_manager\
            .check_status_of_plugin_with_name("droplet_planning_plugin")

    def find_droplet_planning_plugins(self):
        return self.ms.plugin_manager\
            .find_plugin_by_name("droplet_planning_plugin")

    def route_options(self):
        return self.ms.get_state_sync("routes-model", "route-options")

    def routes(self):
        return self.ms.get_state_sync("routes-model", "routes")

    def start_droplet_planning_plugin(self):
        return self.ms.plugin_manager\
            .start_plugin_by_name("droplet_planning_plugin")

    def stop_droplet_planning_plugin(self):
        return self.ms.plugin_manager\
            .stop_plugin_by_name("droplet_planning_plugin")

    def clear_routes(self):
        if self.droplet_planning_is_running() is False:
            self.warn_droplet_planning_plugin_stopped()
            self.start_droplet_planning_plugin()
        msg = None
        success_topic = MicrodropUtils\
            .get_state_topic('routes-model', 'routes')
        return self.ms.trigger_sync('droplet_planning_plugin', 'clear-routes',
                                    msg, success_topic=success_topic)

    def set_routes(self, routes):
        if self.droplet_planning_is_running() is False:
            self.warn_droplet_planning_plugin_stopped()
            self.start_droplet_planning_plugin()
        success_topic = MicrodropUtils.get_state_topic('routes-model',
                                                       'routes')
        return self.ms.put_sync('routes-model', 'routes', routes,
                                success_topic=success_topic)

    def warn_droplet_planning_plugin_stopped(self):
        print("DROPLET PLANNING PLUGIN IS NOT RUNNING")
        print("Attempting to start droplet planning plugin")
