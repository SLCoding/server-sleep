#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import getopt
from ConfigParser import SafeConfigParser
import subprocess
sys.path.append("../classes/")
from log import log

class pingcheck(object):
	"""
check for computers in your network which are running
	"""
	def __init__(self):
		# Read Configfile
		config = SafeConfigParser()
		config.read('pingcheck.cfg')
		self.hostlist = eval(config.get('pingcheck', 'hostlist'), {}, {})
		self.max_hosts = int(config.get('pingcheck', 'max_hosts'))
		self.logger = log()
		
	def __del__(self):
		pass
	
	def check(self):
		try:
			count = 0;
			for host in self.hostlist:
				ret = subprocess.call("ping -c 2 %s" % host,
					shell=True,
					stdout=open('/dev/null', 'w'),
					stderr=subprocess.STDOUT
				)
				if ret == 0:
					self.logger.log("Pingcheck: Host "+ ip +" is up!")
					count += 1
					if count>self.max_hosts:
						self.logger.log("Pingcheck: Not Ready for sleep! More hosts active then allowed!", 2)
						return 1
				else:
					self.logger.log("Pingcheck: Host "+ ip +" is down!")
					
			self.logger.log("Pingcheck: Ready for sleep!")
			return 0
		except:
			return -1
	
	@staticmethod
	def run():
		instance = pingcheck()
		instance.logger.log ("Pingcheck: check started")
		return instance.check()
	
	@staticmethod
	def configure():
		pass


# for testing purpose
if __name__ == '__main__':
	print pingcheck.run()
	pingcheck.configure()
	print pingcheck.__doc__