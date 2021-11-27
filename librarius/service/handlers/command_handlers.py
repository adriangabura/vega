import typing as tp
import logging
from librarius.service.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models
from librarius.service import ensure
from librarius.service.ensure import exceptions

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.domain.messages import AbstractCommand

logger = logging.getLogger(__name__)


class CreateResourceHandler(AbstractCommandHandler[commands.CreateResource]):
    def __call__(self, cmd: "commands.CreateResource"):
        with self.uow:
            resource = self.uow.context.session.query(models.Resource).filter_by(name=cmd.name).first()
            if resource is None:
                resource = models.Resource(uuid=cmd.resource_uuid, name=cmd.name)
                self.uow.repositories.resources.add(resource)
            self.uow.commit()


class CreateRoleGroupHandler(AbstractCommandHandler[commands.CreateRoleGroup]):
    def __call__(self, cmd: "commands.CreateRoleGroup"):
        with self.uow:
            role_group = self.uow.repositories.role_groups.find_by_name(cmd.name)
            if role_group is None:
                role_group = models.RoleGroup(uuid=cmd.role_group_uuid, name=cmd.name)
                for role_name in cmd.role_names:
                    _role = self.uow.repositories.roles.find_by_name(name=role_name)
                    role_group.roles.append(_role)
                self.uow.repositories.role_groups.add(role_group)
            self.uow.commit()
            for role_name in cmd.role_names:
                self.uow.casbin_enforcer.add_grouping_policy(cmd.name, role_name, "*")
            self.uow.casbin_enforcer.save_policy()


class CreateRoleHandler(AbstractCommandHandler[commands.CreateRole]):
    def __call__(self, cmd: "commands.CreateRole"):
        with self.uow:
            role = self.uow.repositories.roles.find_by_name(cmd.name)
            if role is None:
                role = models.Role(uuid=cmd.role_uuid, name=cmd.name)
                for resource_name in cmd.resource_names:
                    _resource = self.uow.repositories.resources.find_by_name(name=resource_name)
                    role.resources.append(_resource)
                self.uow.repositories.roles.add(role)
            self.uow.commit()
            for resource_name in cmd.resource_names:
                self.uow.casbin_enforcer.add_policy(cmd.name, resource_name, "*",)
            self.uow.casbin_enforcer.save_policy()


class CreateUserHandler(AbstractCommandHandler[commands.CreateUser]):
    def __call__(self, cmd: "commands.CreateUser"):
        with self.uow:
            user = self.uow.repositories.users.find_by_username(cmd.name)
            if user is None:
                user = models.User(uuid=cmd.user_uuid, name=cmd.name)
                for role_name in cmd.roles:
                    _role = self.uow.repositories.roles.find_by_name(name=role_name)
                    user.roles.append(_role)
                self.uow.repositories.roles.add(_role)
            self.uow.commit()
            for role_name in cmd.roles:
                self.uow.casbin_enforcer.add_role_for_user(user=cmd.name, role=role_name)
            self.uow.casbin_enforcer.save_policy()



class CreateAuthorHandler(AbstractCommandHandler[commands.CreateAuthor]):
    def __call__(self, cmd: "commands.CreateAuthor"):
        with self.uow:
            author = self.uow.repositories.authors.find_by_uuid(cmd.author_uuid)
            if author is None:
                author = models.Author(uuid=cmd.author_uuid, name=cmd.name)
                self.uow.repositories.authors.add(author)
            self.uow.commit()


class CreateSeriesHandler(AbstractCommandHandler[commands.CreateSeries]):
    def __call__(self, cmd: "commands.CreateSeries"):
        with self.uow:
            series = self.uow.repositories.series.find_by_uuid(cmd.series_uuid)
            if series is not None:
                logger.warning("Series exists!")
            else:
                series = models.Series(uuid=cmd.series_uuid, name=cmd.series_name)
                self.uow.repositories.series.add(series)
            self.uow.commit()
            # Consider returns!


class AddAuthorToPublicationHandler(
    AbstractCommandHandler[commands.AddAuthorToPublication]
):
    def __call__(self, cmd: "commands.AddAuthorToPublication"):
        with self.uow:
            publication = self.uow.repositories.publications.find_by_uuid(
                cmd.author_uuid
            )

            if publication is not None:
                author = self.uow.repositories.authors.find_by_uuid(cmd.author_uuid)
                if author is None:
                    author = models.Author(uuid=cmd.author_uuid, name=cmd.author_name)

                publication.add_author(author)

                # Maybe return result?
            else:
                pass
                # Maybe return result?
            self.uow.commit()


class AddPublicationHandler(AbstractCommandHandler[commands.CreatePublication]):
    def __call__(self, cmd: "commands.CreatePublication"):
        with self.uow:
            publication = self.uow.repositories.publications.find_by_uuid(
                cmd.publication_uuid
            )

            if publication is None:
                publication = models.Publication(
                    title=cmd.title, uuid=cmd.publication_uuid
                )
            self.uow.repositories.publications.add(publication)

            self.uow.commit()

            # Consider returning results!!!


class RemovePublicationHandler(AbstractCommandHandler[commands.RemovePublication]):
    def __call__(self, cmd: "commands.RemovePublication"):
        pass


class AddPublicationToSeriesHandler(
    AbstractCommandHandler[commands.AddPublicationToSeries]
):
    def __call__(self, cmd: "commands.AddPublicationToSeries"):
        with self.uow:
            series = self.uow.repositories.series.find_by_uuid(cmd.series_uuid)
            if series is not None:
                publication = self.uow.repositories.publications.find_by_uuid(
                    cmd.publication_uuid
                )
                if publication is not None:
                    series.add_publication(publication)
                else:
                    logger.warning("No such publication exists!")

            self.uow.commit()
            # Consider returning results!


COMMAND_HANDLERS: tp.Mapping[
    tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]
] = {
    commands.CreateRoleGroup: CreateRoleGroupHandler,
    commands.CreateUser: CreateUserHandler,
    commands.CreateResource: CreateResourceHandler,
    commands.CreateRole: CreateRoleHandler,
    commands.CreateAuthor: CreateAuthorHandler,
    commands.CreatePublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler,
    commands.CreateSeries: CreateSeriesHandler,
    commands.AddPublicationToSeries: AddPublicationToSeriesHandler,
}
