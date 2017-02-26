#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, signal, subprocess, re
from ConfigParser import SafeConfigParser

sys.path.append("../classes/")
from log import log


class proccheck(object):
    """
Write what your check do here!
    """

    def __init__(self):
        # Read Configfile
        config = SafeConfigParser()
        config.read('check-modules/proccheck.cfg')

        # add your options here like this:
        self.procs = eval(config.get('proccheck', 'procs'), {}, {})

        self.logger = log()

    def __del__(self):
        pass

    def check(self):
        try:
            s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
            for process in s.stdout:
                for proc in self.procs:
                    pass
                    if re.search(proc, process):
                        self.logger.log("Proccheck: Process found '" + proc + "'!")
                        self.logger.log("Proccheck: Not ready for sleep!")
                        return 1

            self.logger.log("Proccheck: Ready for sleep!")
            return 0
        except:
            self.logger.log("Proccheck: An unexpected error occured!", 1)
            return -1

    @staticmethod
    def run():
        instance = proccheck()
        instance.logger.log("Proccheck: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        # add the configfile option you used here also
        # configurable.append([sectionname, optionname, defaultvalue, description])
        configurable.append(["proccheck", "procs", '0', "Regular Expressions for the processes to check for"])
        return configurable


# for testing purpose
# if you run "python example.py" the important functions will be executed
if __name__ == '__main__':
    os.chdir('../')
    print(proccheck.run())
    print(proccheck.configure())
    print(proccheck.__doc__)
