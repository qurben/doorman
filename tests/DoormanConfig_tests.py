import unittest, tempfile

from doorman.doorman import DoormanConfig, DoormanException

class DoormanConfigTest(unittest.TestCase):
    """
    Test the DoormanConfig class
    """

    def setUp(self):
        """
        Setup the temporary files
        """
        self.yml = tempfile.NamedTemporaryFile()
        self.txt = tempfile.NamedTemporaryFile()
        self.txt2 = tempfile.NamedTemporaryFile()

    def test_parseYAML_one_password(self):
        """
        Test parsing a single file and a single password
        """
        self.yml.write("""%s:
 pass: yaml""" % self.txt.name)
        self.yml.seek(0)

        parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(parsed, {self.txt.name: {'pass': 'yaml'}})

    def test_parseYAML_multiple_passwords(self):
        """
        Test parsing a single file and multiple passwords
        """
        self.yml.write("""%s:
 pass: yaml
 pass2: yaml2""" % self.txt.name)
        self.yml.seek(0)

        parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(parsed, {self.txt.name: {'pass': 'yaml', 'pass2': 'yaml2'}})

    def test_parseYAML_multiple_files(self):
        """
        Test parsing multiple files and a single password
        """
        self.yml.write("""%s:
 pass: yaml
%s:
 pass2: yaml2""" % (self.txt.name, self.txt2.name))
        self.yml.seek(0)

        parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(parsed, {self.txt.name: {'pass': 'yaml'}, self.txt2.name: {'pass2': 'yaml2'}})

    def test_parseYAML_empty(self):
        """
        Test parsing an empty file
        """
        with self.assertRaises(DoormanException) as e:
            parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(e.exception.name, "parse : empty config")

    def test_parseYAML_invalid(self):
        """
        Test parsing an invalid file

        Note: This is mostly left to the yaml library, it is assumed that a proper YAML file returns a proper dict.
        """
        self.yml.write("\t")
        self.yml.seek(0)

        with self.assertRaises(DoormanException) as e:
            parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(e.exception.name, "parse : Error parsing config YAML")

    def test_parseYAML_not_found(self):
        """
        Test parsing a non-existant file
        """
        self.txt.close() # removes the file
        self.yml.write("""%s:
 pass: yaml""" % self.txt.name)
        self.yml.seek(0)

        with self.assertRaises(DoormanException) as e:
            parsed = DoormanConfig(self.yml.name).parseYAML()

        self.assertEqual(e.exception.name, "parse : File in config not found")
