"""BEMServer API client resources

/event_levels/ endpoints
/event_categories/ endpoints
/events/ endpoints
/events_by_sites/ endpoints
/events_by_buildings/ endpoints
/events_by_storeys/ endpoints
/events_by_spaces/ endpoints
/events_by_zones/ endpoints
"""
from .base import BaseResources


class EventLevelResources(BaseResources):
    endpoint_base_uri = "/event_levels/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EventCategoryResources(BaseResources):
    endpoint_base_uri = "/event_categories/"


class EventResources(BaseResources):
    endpoint_base_uri = "/events/"


class EventBySiteResources(BaseResources):
    endpoint_base_uri = "/events_by_sites/"
    disabled_endpoints = ["update"]


class EventByBuildingResources(BaseResources):
    endpoint_base_uri = "/events_by_buildings/"
    disabled_endpoints = ["update"]


class EventByStoreyResources(BaseResources):
    endpoint_base_uri = "/events_by_storeys/"
    disabled_endpoints = ["update"]


class EventBySpaceResources(BaseResources):
    endpoint_base_uri = "/events_by_spaces/"
    disabled_endpoints = ["update"]


class EventByZoneResources(BaseResources):
    endpoint_base_uri = "/events_by_zones/"
    disabled_endpoints = ["update"]