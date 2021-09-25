import typing as tp

if tp.TYPE_CHECKING:
    from librarius.domain.messages import events, queries, commands

AuthorMessage = tp.Union['events.AuthorAdded', 'queries.AllAuthors', 'queries.AuthorByUuid', 'commands.CreateAuthor']
