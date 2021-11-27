import pytest

from librarius.config.app import BasicConfig
from librarius.utils import load_env_file
from librarius.paths import __DEFAULT_ENV__


@pytest.fixture(scope="session")
def config() -> BasicConfig:
    load_env_file(__DEFAULT_ENV__)
    return BasicConfig()
