from librarius.domain.models.entity import Entity
from librarius.domain.models.author import Author
from librarius.domain.models.publication import Publication
from librarius.domain.models.series import Series


def test_entity():
    assert Entity()


def test_author():
    assert Author()


def test_book():
    assert Publication()


def test_series():
    assert Series()
