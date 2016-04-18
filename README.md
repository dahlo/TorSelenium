# TorSelenium
Create multiple Firefox browser with Selenium that each runs through a separate Tor proxy. This class will spawn the specified number of Tor proxies and create a Selenium Firefox browers that runs through each of the proxies, giving them all separate IPs.

# Requirements (Ubuntu 14.04)
```bash
sudo apt-get install python-dev python-pip tor
sudo pip install selenium psutil
```

# Example
```python
#!/bin/env python
from TorSelenium import TorSelenium

# create TorSelenium object
test = TorSelenium()

# create browsers
test.create_tor_browsers(3)

# get IP of each browser
for browser in test.browsers:
	browser.get("http://myexternalip.com/raw")

# kill running proxies
test.kill_running_proxies()
```

