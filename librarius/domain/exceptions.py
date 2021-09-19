class SkipMessage (Exception):
    """
    This exception is raised when a message can't be processed, but there's no
    incorrect behavior. For example, we might receive the same message multiple
    times, or we might receive a message that is now out of date.
    """

    def __init__(self, reason: str):
        self.reason = reason
