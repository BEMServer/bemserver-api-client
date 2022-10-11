"""BEMServer API client resources

/event_states/ endpoints
/event_levels/ endpoints
/event_categories/ endpoints
/events/ endpoints
"""
from .base import BaseResources


class EventStateResources(BaseResources):
    endpoint_base_uri = "/event_states/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EventLevelResources(BaseResources):
    endpoint_base_uri = "/event_levels/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EventCategoryResources(BaseResources):
    endpoint_base_uri = "/event_categories/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EventResources(BaseResources):
    endpoint_base_uri = "/events/"
