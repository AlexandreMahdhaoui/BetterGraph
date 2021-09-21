import pytest


class TestMutationResolver:

    @pytest.fixture()
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass