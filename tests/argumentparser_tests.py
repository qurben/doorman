import unittest, os, mock

import doorman.main

class ArgumentParserTests(unittest.TestCase):
	"""
	Test the argument parser
	"""

	def test_argumentparser_mutually_exclusive(self):
		"""
		Test that -u and -s are mutually exclusive
		"""
		devnull = open(os.devnull, 'wb')
		with mock.patch('sys.stderr', devnull): #redirect stderr to devnull
			with self.assertRaises(SystemExit) as err:
				doorman.main.create_parser().parse_args(["-u","-s"])

	def test_argumentparser_unsecret(self):
		"""
		Test that -u is going to unsecret the file
		"""
		args = doorman.main.create_parser().parse_args(["-u"])

		self.assertEquals(args.status, False)
		self.assertEquals(args.config_file, doorman.main.DEFAULT_CONFIG_FILE)

	def test_argumentparser_secret(self):
		"""
		Test that -s is going to secret the file
		"""
		args = doorman.main.create_parser().parse_args(["-s"])
		self.assertEquals(args.status, True)