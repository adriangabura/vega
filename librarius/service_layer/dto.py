import attr


@attr.s
class AuthorDto:
    uuid: str = attr.field()
    name: str = attr.field()

    def as_dict(self):
        return attr.asdict(self)

