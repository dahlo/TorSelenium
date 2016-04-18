from selenium import webdriver
import subprocess
import os
import psutil



class TorSelenium(object):

	def __init__(self):

		# settings
		self.base_socks_port = 9150
		self.base_control_port = 8118
		self.base_dir = "/tmp/data"
		self.browsers = []


	def create_tor_browsers(self, n_instances):

		# start the tor proxies
		self.start_tor_proxies(n_instances)

		# create the browsers
		self.browsers = []
		for i in range(n_instances):

			# create a profile with the correct proxy settings
			profile = webdriver.FirefoxProfile()
			profile.set_preference('network.proxy.type', 1)
			profile.set_preference('network.proxy.socks', '127.0.0.1')
			profile.set_preference('network.proxy.socks_port', self.base_socks_port+i)
			self.browsers.append(webdriver.Firefox(profile))



	def start_tor_proxies(self, n_instances):

		# create base directory if not existing
		if not os.path.isdir(self.base_dir):
			os.makedirs(self.base_dir)


		# start each proxy
		for i in range(n_instances):

			# define this instance's ports
			socks_port = self.base_socks_port + i
			control_port = self.base_control_port + i

			# create instance directory if not existing
			if not os.path.isdir("%s/tor%s" % (self.base_dir, i)):
				os.makedirs("%s/tor%s" % (self.base_dir, i))


			# start the tor proxy
			command = "	tor --RunAsDaemon 1 --CookieAuthentication 0 --HashedControlPassword '' --ControlPort %s --PidFile tor%s.pid --SocksPort %s --DataDirectory %s/tor%s" % (control_port, i, socks_port, self.base_dir, i)
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()





	def kill_running_proxies(self):

		for proc in psutil.process_iter():
			if " ".join(proc.cmdline()).startswith('tor --RunAsDaemon 1 --CookieAuthentication 0 --HashedControlPassword'):
				proc.kill()


if __name__ == '__main__':

	# create TorBrowser object
	test = TorSelenium()
	
	# create browsers
	test.create_tor_browsers(3)

	# gert IP of each browser
	for browser in test.browsers:
		browser.get("http://myexternalip.com/raw")

	# kill running proxies
	test.kill_running_proxies()
