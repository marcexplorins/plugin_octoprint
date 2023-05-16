# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import requests

##  https://8a15-79-155-18-236.ngrok-free.app
BACKEND_URL = 'https://nano-backend.eu.ngrok.io'

class NanostorePlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin
):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/nanostore.js"],
            "css": ["css/nanostore.css"],
            "less": ["less/nanostore.less"]
        }

    ##~~ Softwareupdate hook


    def on_event(self, event, payload):
        output_parts = [u"event ................................................. : {payload}"]

        if event == 'SlicingStarted':
            
            filename = payload['stl']
            gcode = payload['gcode']
            gcode_location = payload['gcode_location']

            if not filename.startswith('nanostore_'):
                return

            self._logger.info("Hello SlicingStarted | " + filename)

            payload = {'filename': filename, 'gcode': gcode, 'gcode_location': gcode_location}
            url = BACKEND_URL + '/slice-event'
            r = requests.post(url, json = payload)

        if event == 'SlicingDone':
            filename = payload['stl']
            gcode = payload['gcode']
            gcode_location = payload['gcode_location']

            if not filename.startswith('nanostore_'):
                return
            
            self._logger.info("Hello SlicingDone | " + filename)

            payload = {'filename': filename, 'gcode': gcode, 'gcode_location': gcode_location}
            url = BACKEND_URL + '/slice-event/sliceOK'
            r = requests.post(url, json = payload)

        if event == 'PrintStarted':
            filename = payload['name']

            if not filename.startswith('nanostore_'):
                return
            
            self._logger.info("Nanostore PrintStarted | " + filename)
            payload = {'filename': filename}
            url = BACKEND_URL + '/print-event/printStart'
            r = requests.post(url, data=payload)

        if event == 'PrintDone':
            filename = payload['name']

            if not filename.startswith('nanostore_'):
                return
            
            self._logger.info("Nanostore PrintDone | " + filename)
            payload = {'filename': filename}
            url = BACKEND_URL + '/print-event/printOK'
            r = requests.post(url, data=payload)

        if event == 'PrintFailed':
            filename = payload['name']

            if not filename.startswith('nanostore_'):
                return
            
            self._logger.info("Nanostore PrintFailed | " + filename)
            payload = {'filename': filename}
            url = BACKEND_URL + '/print-event/printKO'
            r = requests.post(url, data=payload)


        if event == 'MetadataAnalysisFinished':
            filename = payload['name']
            result = payload['result']

            if not filename.startswith('nanostore_'):
                return
            
            self._logger.info("Nanostore MetadataAnalysisFinished | " + filename)
            
            payload = {'filename': filename, 'result': result}
            url = BACKEND_URL + '/slice-event/metadata-done'
            r = requests.post(url, data=payload)

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "nanostore": {
                "displayName": "Nanostore Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "you",
                "repo": "OctoPrint-Nanostore",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/you/OctoPrint-Nanostore/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Nanostore Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = NanostorePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
