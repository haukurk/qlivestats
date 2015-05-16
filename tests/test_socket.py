from unittest import TestCase

from tests import tests_dir
os.chdir(tests_dir)

class SocketTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(BasicConfigTest, self).__init__(*args, **kwargs)

    def test_read_socket(self):
        # hehe






