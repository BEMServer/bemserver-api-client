"""BEMServer API client event resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    EventResources,
    EventStateResources,
    EventLevelResources,
    EventCategoryResources,
)


class TestAPIClientResourcesEvents:
    def test_api_client_resources_events(self):
        assert issubclass(EventResources, BaseResources)
        assert EventResources.endpoint_base_uri == "/events/"
        assert EventResources.disabled_endpoints == []

        assert issubclass(EventStateResources, BaseResources)
        assert EventStateResources.endpoint_base_uri == "/event_states/"
        assert EventStateResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]

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
        assert EventCategoryResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]