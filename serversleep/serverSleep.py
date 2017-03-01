#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time
import importlib

import configparser
import logging
from server_sleep_api import PluginInterface


class serverSleep(object):
    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('server-sleep.cfg')
        self.checkinterval = int(config.get('serverSleep', 'checkinterval'))
        self.sleepcmd = config.get('serverSleep', 'sleepcmd')
        self.enabledmodules = eval(config.get('serverSleep', 'enabledmodules'))
        self.plugins = []
        self.logger = logging.getLogger(__name__)

        for enabledmodule in self.enabledmodules:
            module = importlib.import_module("server_sleep_coreplugins.coreplugins." + enabledmodule, enabledmodule)
            plugin = getattr(module, enabledmodule)()
            if isinstance(plugin, PluginInterface.AbstractCheckPlugin):
                self.plugins.append(plugin)
                self.logger.info("Module loaded: " + enabledmodule)
            else:
                self.logger.warning("Loaded Module appears to be no CheckPlugin: " + enabledmodule)

    def __del__(self):
        pass

    def startup(self):
        while True:
            self.logger.info("Wait " + str(self.checkinterval) + " seconds...")
            time.sleep(self.checkinterval)

            result = True

            self.logger.info("Checks started")
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
                    self.logger.error(pluginName + " failed!", 1)

            if not result:
                continue

            self.logger.info("All Checks OK: Going to Sleep Now!")
            for plugin in self.plugins:
                try:
                    plugin.pre_sleep()
                except NotImplementedError:
                    pass

            os.system(self.sleepcmd);

            self.logger.info("Sleep is over: Server woke up!")
            for plugin in self.plugins:
                try:
                    plugin.post_sleep()
                except NotImplementedError:
                    pass

