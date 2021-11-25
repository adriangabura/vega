import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


def test_supergroup_role(supergroup_role):
    pass