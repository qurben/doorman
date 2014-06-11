import unittest, os, mock

import doorman.main

class ArgumentParserTests(unittest.TestCase):

	def test_argumentparser_mutually_exclusive(self):
		devnull = open(os.devnull, 'wb')
		with mock.patch('sys.stderr', devnull): #redirect stderr to devnull
			with self.assertRaises(SystemExit) as err:
				doorman.main.create_parser().parse_args(["-u","-s"])

	def test_argumentparser_unsecret(self):
		args = doorman.main.create_parser().parse_args(["-u"])

		self.assertEquals(args.status, False)
		self.assertEquals(args.config_file, doorman.main.DEFAULT_CONFIG_FILE)

	def test_argumentparser_secret(self):
		args = doorman.main.create_parser().parse_args(["-s"])
		self.assertEquals(args.status, True)