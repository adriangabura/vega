from librarius.service.dto import AuthorDto
from librarius.domain import models


class AuthorAssembler:
    @staticmethod
    def from_dto(dto: "AuthorDto"):
        return models.Author(**dto.as_dict())
