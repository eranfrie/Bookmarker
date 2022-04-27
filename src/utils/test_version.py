from utils import version


# pylint: disable=R0201 (no-self-use)
class TestVersion:
    def test_version(self):
        """
        just run it and check it returns (some) value.
        """
        assert version.get_version()

    def test_version_mock_patch(self):
        """
        override get_patch() and compare version.
        """
        patch_func = version.get_patch()
        version.get_patch = lambda: "test_patch"
        assert version.get_version() == f"{version.MAJOR}.{version.MINOR}.test_patch"
        version.get_patch = patch_func
