"""Version tests"""
from bemserver_api_client import __version__


class TestVersion:
    def test_version(self):
        assert __version__ == "0.0.1"
