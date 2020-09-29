from sys import version_info
import platform

assert version_info >= (3,7), "LinkedinScraper requires Python 3.7 or later"
print('You are using ' + platform.python_version())
