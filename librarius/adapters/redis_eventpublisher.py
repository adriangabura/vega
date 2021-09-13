import typing as tp
import json
import logging
from dataclasses import asdict

from librarius.config import config
from librarius.domain import events

logger = logging.getLogger(__name__)

class Butaforie:
    def publish(self, channel, ev):
        pass

r = Butaforie()


def publish(channel, event: events.AbstractEvent) -> tp.NoReturn:
    logging.info(f"publishing: channel={channel}, event={event}")
    r.publish(channel, json.dumps(asdict(event)))
