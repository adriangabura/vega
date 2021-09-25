from pathlib import Path

__LIBRARIUS_ROOT__ = Path(__file__).parent

__DEFAULT_ENV__ = __LIBRARIUS_ROOT__.parent / '.env'

__TESTING_ENV__ = __DEFAULT_ENV__
