import typing as tp
from dotenv import load_dotenv, dotenv_values

if tp.TYPE_CHECKING:
    from pathlib import Path


class PathNotExistsError(Exception):
    """Exception that is raised when the Path doesn't exist."""

    @classmethod
    def with_path(cls, path: "Path"):
        return cls(f"Path: '{path}' not found!")


def check_path_exists(path: "Path") -> tp.Union["Path", tp.NoReturn]:
    """Check whether a path exists and return the path."""
    if not path.exists():
        raise PathNotExistsError.with_path(path)
    return path


def load_env_file(path: "Path", override=False) -> None:
    """Load an env file using a Path."""
    load_dotenv(check_path_exists(path), override=override)


def retrieve_env_values(path: "Path") -> tp.Mapping[str, tp.Optional[str]]:
    """Retrieve a dictionary of key values from an env file using a Path."""
    return dotenv_values(check_path_exists(path))
