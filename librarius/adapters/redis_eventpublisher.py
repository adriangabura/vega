import json
import logging
from dataclasses import asdict

from librarius.domain.messages import AbstractEvent

logger = logging.getLogger(__name__)


class Butaforie:
    def publish(self, channel, ev):
        pass


r = Butaforie()


def publish(channel, event: AbstractEvent) -> None:
    logging.info(f"publishing: channel={channel}, event={event}")
    # r.publish(channel, json.dumps(asdict(event)))
    r.publish(channel, event)
