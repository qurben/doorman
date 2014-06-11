import unittest, tempfile, os
from doorman.doorman import Doorman, DoormanException

class DoormanTest(unittest.TestCase):
    """
    Doorman test class
    """
    def setUp(self):
        self.yml = tempfile.NamedTemporaryFile()
        self.txt = tempfile.NamedTemporaryFile()
        self.txt2 = tempfile.NamedTemporaryFile()

        self.yml.write("""%s:
 pass: hfayjy2w
 pass2: gSJTkzJ3""" % self.txt.name)
        self.yml.seek(0)

    def test_doorman_hide(self):
        self.txt.write("""ahfayjy2wb""")
        self.txt.seek(0)

        dm = Doorman(True, self.yml.name)

        dm.run()

        self.assertEqual("a{{pass}}b", self.txt.read())

    def test_doorman_unhide(self):
        self.txt.write("a{{pass}}b")
        self.txt.seek(0)

        dm = Doorman(False, self.yml.name)
        dm.run()

        self.assertEqual("ahfayjy2wb", self.txt.read())

    def test_doorman_nohide(self):
        self.txt.write("hello")
        self.txt.seek(0)

        dm = Doorman(False, self.yml.name)
        dm.run()

        self.assertEqual("hello", self.txt.read())

    def test_doorman_multiple_hide(self):
        self.txt.write("hfayjy2w and hfayjy2w")
        self.txt.seek(0)

        dm = Doorman(True, self.yml.name)
        dm.run()

        self.assertEqual("{{pass}} and {{pass}}", self.txt.read())

    def test_doorman_multiple_nohide(self):
        self.txt.write("{{pass}} and {{pass}}")
        self.txt.seek(0)

        Doorman(False, self.yml.name).run()

        self.assertEqual("hfayjy2w and hfayjy2w", self.txt.read())

    def test_doorman_different_hide(self):
        self.txt.write("hfayjy2w and gSJTkzJ3")
        self.txt.seek(0)

        Doorman(True, self.yml.name).run()

        self.assertEqual("{{pass}} and {{pass2}}", self.txt.read())

    def test_doorman_different_unhide(self):
        self.txt.write("{{pass}} and {{pass2}}")
        self.txt.seek(0)

        Doorman(False, self.yml.name).run()
        
        self.assertEqual("hfayjy2w and gSJTkzJ3", self.txt.read())

    def test_doorman_readfail(self):
        os.chmod(self.txt.name, 0o200)

        dm = Doorman(True, self.yml.name)
        with self.assertRaises(DoormanException) as e:
            dm.run()

        self.assertEqual(e.exception.name, "File not read")

    def test_doorman_writefail(self):
        os.chmod(self.txt.name, 0o400)

        dm = Doorman(True, self.yml.name)
        with self.assertRaises(DoormanException) as e:
            dm.run()

        self.assertEqual(e.exception.name, "File not write")
