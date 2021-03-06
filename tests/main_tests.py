import unittest, tempfile

import doorman.main

class MainTests(unittest.TestCase):
	"""
	Test the main function mainly tests the is_default_config function
	"""

	def test_is_default_config_true(self):
		"""
		Test if is_default_config returns True with a default config
		"""
		self.yml = tempfile.NamedTemporaryFile()
		self.yml.write(doorman.main.DEFAULT_CONFIG)
		self.yml.seek(0)
		doorman.main.DEFAULT_CONFIG_FILE = self.yml.name
		self.assertEquals(doorman.main.is_default_config(doorman.main.DEFAULT_CONFIG_FILE), True)

	def test_is_default_config_false(self):
		"""
		Test if is_default_config returns False with a default config
		"""
		self.yml = tempfile.NamedTemporaryFile()
		self.yml.write(doorman.main.DEFAULT_CONFIG)
		self.yml.write("test")
		self.yml.seek(0)
		doorman.main.DEFAULT_CONFIG_FILE = self.yml.name
		self.assertEquals(doorman.main.is_default_config(doorman.main.DEFAULT_CONFIG_FILE), False)




