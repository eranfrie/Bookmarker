from utils import version


class TestVersion:
    def test_version(self):
        # just run it and check it has value
        assert version.get_version()

        # override get_patch() and compare version
        patch_func = version.get_patch()
        version.get_patch = lambda: "test_patch"
        assert version.get_version() == f"{version.MAJOR}.{version.MINOR}.test_patch"
        version.get_patch = patch_func
