import hashlib
import base64
import attr


def content_md5(self) -> str:
    content_md5_digest = hashlib.md5(self.binary_body).digest()
    return base64.b64encode(content_md5_digest).decode("utf-8")


@attr.s
class AuthorDto:
    uuid: str = attr.field()
    name: str = attr.field()

    def as_dict(self):
        return attr.asdict(self)


@attr.s
class FileUploadDto:
    body: bytes = attr.field()
    content_md5_hash: str = attr.field()
    content_type: str = attr.field()

    @classmethod
    def from_body(cls, body: bytes, content_type: str):
        content_md5_hash_digest = hashlib.md5(body).digest()
        content_md5_hash = base64.b64encode(content_md5_hash_digest).decode("utf-8")
        return cls(body, content_md5_hash, content_type)
