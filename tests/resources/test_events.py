"""BEMServer API client events resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    EventResources,
    EventLevelResources,
    EventCategoryResources,
    EventBySiteResources,
    EventByBuildingResources,
    EventByStoreyResources,
    EventBySpaceResources,
    EventByZoneResources,
)


class TestAPIClientResourcesEvents:
    def test_api_client_resources_events(self):
        assert issubclass(EventResources, BaseResources)
        assert EventResources.endpoint_base_uri == "/events/"
        assert EventResources.disabled_endpoints == []

        assert issubclass(EventLevelResources, BaseResources)
        assert EventLevelResources.endpoint_base_uri == "/event_levels/"
        assert EventLevelResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]

        assert issubclass(EventCategoryResources, BaseResources)
        assert EventCategoryResources.endpoint_base_uri == "/event_categories/"
        assert EventCategoryResources.disabled_endpoints == []

        assert issubclass(EventBySiteResources, BaseResources)
        assert EventBySiteResources.endpoint_base_uri == "/events_by_sites/"
        assert EventBySiteResources.disabled_endpoints == ["update"]

        assert issubclass(EventByBuildingResources, BaseResources)
        assert EventByBuildingResources.endpoint_base_uri == "/events_by_buildings/"
        assert EventByBuildingResources.disabled_endpoints == ["update"]

        assert issubclass(EventByStoreyResources, BaseResources)
        assert EventByStoreyResources.endpoint_base_uri == "/events_by_storeys/"
        assert EventByStoreyResources.disabled_endpoints == ["update"]

        assert issubclass(EventBySpaceResources, BaseResources)
        assert EventBySpaceResources.endpoint_base_uri == "/events_by_spaces/"
        assert EventBySpaceResources.disabled_endpoints == ["update"]

        assert issubclass(EventByZoneResources, BaseResources)
        assert EventByZoneResources.endpoint_base_uri == "/events_by_zones/"
        assert EventByZoneResources.disabled_endpoints == ["update"]
