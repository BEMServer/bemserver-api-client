"""BEMServer API client resources

/event_levels/ endpoints
/event_categories/ endpoints
/events/ endpoints
/timeseries_by_events/ endpoints
"""
from .base import BaseResources


class EventLevelResources(BaseResources):
    endpoint_base_uri = "/event_levels/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EventCategoryResources(BaseResources):
    endpoint_base_uri = "/event_categories/"


class EventResources(BaseResources):
    endpoint_base_uri = "/events/"
