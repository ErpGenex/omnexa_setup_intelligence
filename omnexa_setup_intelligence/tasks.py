# Copyright (c) 2026, Omnexa and contributors
# License: MIT

from omnexa_setup_intelligence.engine.health import publish_setup_health_snapshot


def daily():
	publish_setup_health_snapshot()
