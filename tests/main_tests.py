import unittest, tempfile

import doorman.main

class MainTests(unittest.TestCase):

	def test_is_default_config_true(self):
		self.yml = tempfile.NamedTemporaryFile()
		self.yml.write(doorman.main.DEFAULT_CONFIG)
		self.yml.seek(0)
		doorman.main.DEFAULT_CONFIG_FILE = self.yml.name
		self.assertEquals(doorman.main.is_default_config(doorman.main.DEFAULT_CONFIG_FILE), True)

	def test_is_default_config_false(self):
		self.yml = tempfile.NamedTemporaryFile()
		self.yml.write(doorman.main.DEFAULT_CONFIG)
		self.yml.write("test")
		self.yml.seek(0)
		doorman.main.DEFAULT_CONFIG_FILE = self.yml.name
		self.assertEquals(doorman.main.is_default_config(doorman.main.DEFAULT_CONFIG_FILE), False)




