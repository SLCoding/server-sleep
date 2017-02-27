#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time
import importlib

import configparser
from server_sleep_api import PluginInterface
from serversleep.log import log


class serverSleep(object):
    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('server-sleep.cfg')
        self.checkinterval = int(config.get('serverSleep', 'checkinterval'))
        self.sleepcmd = config.get('serverSleep', 'sleepcmd')
        self.enabledmodules = eval(config.get('serverSleep', 'enabledmodules'))
        self.plugins = []
        self.logger = log()

        for enabledmodule in self.enabledmodules:
            module = importlib.import_module("serversleep.checkmodules." + enabledmodule, enabledmodule)
            plugin = getattr(module, enabledmodule)()
            if isinstance(plugin, PluginInterface.AbstractCheckPlugin):
                self.plugins.append(plugin)
                self.logger.log("Module loaded: " + enabledmodule, 3, True)
            else:
                self.logger.log("Loaded Module appears to be no CheckPlugin: " + enabledmodule, 1, True)

    def __del__(self):
        pass

    def startup(self):
        while True:
            self.logger.log("Wait " + str(self.checkinterval) + " seconds...")
            time.sleep(self.checkinterval)

            result = True

            self.logger.log("Checks started")
            status = None
            for plugin in self.plugins:
                pluginName = plugin.__class__.__name__
                status = plugin.check()

                if status == 1:
                    result = False
                elif status == 2:
                    result = True
                    break
                elif status == -1:
                    self.logger.log(pluginName + " failed!", 1)

            if not result:
                continue

            self.logger.log("All Checks OK: Going to Sleep Now!", 3, True)
            os.system(self.sleepcmd);
            self.logger.log("Sleep is over: Server woke up!", 3, True)
